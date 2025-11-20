import streamlit as st
from config import CUSTOM_ICON_URL

# 1. Page Configuration
# Must be the very first Streamlit command.
st.set_page_config(
    page_title="Alexandre dos Santos Library",
    page_icon=CUSTOM_ICON_URL, 
    layout="wide", 
    initial_sidebar_state="collapsed",
)

# 2. Imports
# Imported after page_config to avoid Streamlit errors.
from views import (
    apply_custom_styles, 
    render_logo_and_title, 
    render_home_tab, 
    render_live_tab, 
    render_bookings_tab, 
    render_profile_tab, 
    render_admin_tab
)
from auth import check_login_status

# 3. Initialization & Global Styles
apply_custom_styles()     # Inject CSS for dark mode and custom UI elements
render_logo_and_title()   # Render the header (visible on login and main app)
check_login_status()      # Verify user session; halts execution here if not logged in.

# 4. Role-Based Routing
# Logic to determine which dashboard to show based on user role.
user_role = st.session_state.get('user_role', 'Student')

# Layout: Centered tabs with spacers on the side for aesthetic balance
left_spacer, tabs_col, right_spacer = st.columns([1, 6, 1])

with tabs_col:
    if user_role == "Librarian":
        # --- ADMIN VIEW ---
        tab_home, tab_live, tab_admin = st.tabs(["Home", "Live 💡", "Admin Dashboard 👮"])
        
        with tab_home: render_home_tab()
        with tab_live: render_live_tab()
        with tab_admin: render_admin_tab()
        
    else:
        # --- STUDENT VIEW ---
        tab_home, tab_live, tab_bookings, tab_profile = st.tabs(["Home", "Live", "Bookings", "Profile"])
        
        with tab_home: render_home_tab()
        with tab_live: render_live_tab()
        with tab_bookings: render_bookings_tab()
        with tab_profile: render_profile_tab()