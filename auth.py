import streamlit as st
import random
import base64
import hashlib
from config import PORTUGUESE_FIRST_NAMES, PORTUGUESE_SURNAMES, ADMIN_EMAIL
from data_manager import load_student_ids, save_student_ids

def hash_password(password):
    """
    Securely hashes the password using SHA-256.
    This ensures we never store passwords in plain text in the JSON file.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def derive_user_identity(email, initial_password=None):
    """
    Determines user role and identity. 
    If user exists in JSON, load them.
    If user is new, generate a mock identity based on email structure.
    """
    # 1. ADMIN CHECK
    if email == ADMIN_EMAIL:
        return "ADMIN", "Librarian", "Library Administrator", None

    prefix = email.split('@')[0]
    user_data = load_student_ids()
    
    # 2. EXISTING USER CHECK
    if email in user_data:
        data = user_data[email]
        return data['id'], data['role'], data['display_name'], data['password']

    # 3. NEW ACCOUNT REGISTRATION (Mock Logic)
    if prefix.isdigit():
        role = "Student"
        new_id = prefix
        first_name = random.choice(PORTUGUESE_FIRST_NAMES)
        surname = random.choice(PORTUGUESE_SURNAMES)
        new_name = f"{first_name} {surname}"
    else:
        role = "Professor"
        new_id = str(random.randint(10000, 99999)) 
        new_name = prefix.replace('.', ' ').title()
    
    # Save new user to DB with HASHED password
    hashed_pw = hash_password(initial_password) if initial_password else None
    
    data = {
        'id': new_id,
        'role': role,
        'display_name': new_name,
        'password': hashed_pw 
    }
    user_data[email] = data
    save_student_ids(user_data)
    
    return new_id, role, new_name, hashed_pw

def update_user_password(email, new_password):
    """Updates password in JSON storage after hashing it."""
    user_data = load_student_ids()
    if email in user_data:
        user_data[email]['password'] = hash_password(new_password)
        save_student_ids(user_data)
        return True
    return False

def update_profile_picture(email, uploaded_file):
    """Converts uploaded image to Base64 string and saves to JSON."""
    if uploaded_file is None: return False
    try:
        bytes_data = uploaded_file.getvalue()
        b64_string = base64.b64encode(bytes_data).decode('utf-8')
        user_data = load_student_ids()
        if email in user_data:
            user_data[email]['profile_pic'] = b64_string
            save_student_ids(user_data)
            return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False
    return False

def login_page():
    """Renders the Login UI."""
    st.markdown("<h3 style='text-align: center;'>Student/Faculty Access</h3>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        email_input = st.text_input("University Email")
        password_input = st.text_input("Password", type="password")
        
        user_data_all = load_student_ids()
        is_known_user = email_input in user_data_all
        stored_password_hash = user_data_all.get(email_input, {}).get('password')
        
        if st.button("Log In", use_container_width=True):
            # Validation
            if email_input != ADMIN_EMAIL and not email_input.endswith("@novasbe.pt"):
                 st.error("Invalid email domain. Must be @novasbe.pt")
                 return
            if len(password_input) < 1:
                st.error("Password cannot be empty.")
                return
            
            # Check Password
            if is_known_user:
                input_hash = hash_password(password_input)
                if input_hash != stored_password_hash:
                    st.error("Invalid password for this account.")
                    return
            
            # Success: Set Session State
            student_id, role, display_name, final_password = derive_user_identity(email_input, password_input)
            st.session_state.user_email = email_input
            st.session_state.student_number = student_id
            st.session_state.user_role = role 
            st.session_state.display_name = display_name 
            st.session_state.logged_in = True
            st.rerun()

def check_login_status():
    """Session Guard: Checks if user is logged in, otherwise renders Login Page."""
    # Initialize default state if not present
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if 'student_number' not in st.session_state: st.session_state.student_number = "N/A"
    if 'user_email' not in st.session_state: st.session_state.user_email = "N/A"
    if 'user_role' not in st.session_state: st.session_state.user_role = "N/A"
    if 'display_name' not in st.session_state: st.session_state.display_name = "User"

    if not st.session_state.logged_in:
        login_page()
        st.stop() # Stop main.py execution here