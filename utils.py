import random
import string
import math
import qrcode 
from io import BytesIO 
from datetime import datetime
from config import LIBRARY_TIMEZONE
import streamlit as st

def generate_checkin_code(length=3):
    """Generates a random alphanumeric code (e.g., 'A7X') for check-in verification."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_qr_image(code):
    """
    Generates a QR Code image from the check-in string.
    Returns a BytesIO object (in-memory image) for Streamlit to render.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(code)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer

# ==========================================
# 📡 LIVE MAP SIMULATION ALGORITHMS
# ==========================================

def get_target_occupancy(hour):
    """
    Uses a Gaussian (Bell Curve) function to simulate realistic library crowds.
    - Peak: 14:00 (2 PM)
    - Spread: 4 hours
    - Max Occupancy: 85%
    """
    if hour < 8 or hour >= 20:
        return 0.0 
    
    peak_hour = 14
    max_occupancy = 0.85
    spread = 4 
    
    # Gaussian Formula
    occupancy = max_occupancy * math.exp(-0.5 * ((hour - peak_hour) / spread) ** 2)
    return max(0.1, occupancy) 

def update_seat_simulation(current_states, all_seats):
    """
    Updates seat statuses ('Occupied'/'Available') based on probability.
    Includes 'stickiness' so seats don't flicker randomly every second.
    """
    now_hour = datetime.now(LIBRARY_TIMEZONE).hour
    
    # Reset if closed
    if now_hour >= 20 or now_hour < 8:
        return {seat_id: "Available" for seat_id in all_seats}

    target_occupancy = get_target_occupancy(now_hour)
    new_states = current_states.copy()
    
    # Initial Population
    if not new_states:
        for seat_id in all_seats:
            if random.random() < target_occupancy:
                new_states[seat_id] = "Occupied"
            else:
                new_states[seat_id] = "Available"
        return new_states

    # Iterative Updates (Stickiness Logic)
    for seat_id in all_seats:
        current_status = new_states.get(seat_id, "Available")
        
        if current_status == "Occupied":
            # 5% chance to leave
            if random.random() < 0.05: 
                new_states[seat_id] = "Available"
        else:
            # Calculate current global occupancy
            current_total_occupied = sum(1 for s in new_states.values() if s == "Occupied")
            current_rate = current_total_occupied / len(all_seats)
            
            # If below target curve, higher chance to arrive (10%)
            # If above target curve, lower chance to arrive (1%)
            if current_rate < target_occupancy:
                if random.random() < 0.10:
                    new_states[seat_id] = "Occupied"
            else:
                if random.random() < 0.01:
                    new_states[seat_id] = "Occupied"
                    
    return new_states

def get_current_time():
    """
    Returns the current time, OR a fake debug time if set in the Admin panel.
    replaces: datetime.now(LIBRARY_TIMEZONE)
    """
    # Check if a fake time is set in session state
    if 'debug_time' in st.session_state and st.session_state.debug_time:
        return st.session_state.debug_time
    
    # Otherwise return real time
    return datetime.now(LIBRARY_TIMEZONE)