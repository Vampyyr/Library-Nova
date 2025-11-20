import json
import os
import streamlit as st
from datetime import datetime, timedelta
from config import DB_FILE, STUDENT_DB_FILE, LIBRARY_TIMEZONE

def load_student_ids():
    """Loads student credentials and profiles from JSON storage."""
    if not os.path.exists(STUDENT_DB_FILE):
        return {}
    try:
        with open(STUDENT_DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_student_ids(data):
    """Persists new user registrations or profile updates."""
    with open(STUDENT_DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    """
    Loads booking data and sanitizes fields (e.g., ensuring check_in_time exists).
    """
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            try:
                data = json.load(f)
                # Data sanitization loop
                for booking in data:
                    booking['status'] = booking.get('status', 'Confirmed')
                    val = booking.get('check_in_time')
                    booking['check_in_time'] = val if val not in ('None', None) else None
                return data
            except json.JSONDecodeError:
                return []
    except IOError:
        return []

def save_data(bookings):
    """Writes the list of booking dictionaries to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(bookings, f, indent=4)

def cleanup_and_update_bookings(bookings):
    """
    CRITICAL FUNCTION:
    1. Checks for expired bookings (End time passed -> Completed).
    2. Checks for No-Shows (Start time + 15mins passed without check-in -> No-Show).
    Returns the updated list of bookings.
    """
    updated = False
    now = datetime.now(LIBRARY_TIMEZONE)
    
    for booking in bookings:
        current_status = booking.get('status', 'Confirmed')
        
        if current_status in ("Confirmed", "Active"):
            # Parse strings back to datetime objects
            start_dt = LIBRARY_TIMEZONE.localize(datetime.strptime(f"{booking['date']} {booking['start_time']}", "%Y-%m-%d %H:%M"))
            end_dt = LIBRARY_TIMEZONE.localize(datetime.strptime(f"{booking['date']} {booking['end_time']}", "%Y-%m-%d %H:%M"))
            
            # Logic: If confirmed but not checked in by deadline (15 mins), mark No-Show
            if current_status == "Confirmed":
                no_show_deadline = start_dt + timedelta(minutes=15)
                if now > no_show_deadline:
                    booking['status'] = "No-Show" 
                    updated = True
            
            # Logic: If active and time has passed, mark Completed
            elif current_status == "Active":
                if now > end_dt:
                    booking['status'] = "Completed" 
                    updated = True
            
    if updated:
        save_data(bookings)
    return bookings

def get_eligible_bookings(all_bookings):
    """
    Returns bookings for the current user that are within the 
    allowed check-in window (+/- 15 mins of start time).
    """
    eligible_bookings = []
    now_tz = datetime.now(LIBRARY_TIMEZONE)
    
    for booking in all_bookings:
        # Filter: Current User AND Confirmed Status
        if booking.get('user_email') == st.session_state.user_email and booking.get('status', 'Confirmed') == 'Confirmed':
            start_dt = LIBRARY_TIMEZONE.localize(datetime.strptime(f"{booking['date']} {booking['start_time']}", "%Y-%m-%d %H:%M"))
            min_checkin = start_dt - timedelta(minutes=15)
            max_checkin = start_dt + timedelta(minutes=15)
            
            # Check if current time is within window
            if min_checkin <= now_tz <= max_checkin:
                eligible_bookings.append(booking)
                
    return eligible_bookings