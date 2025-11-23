import json
import os
import streamlit as st
from datetime import datetime, timedelta
from config import DB_FILE, STUDENT_DB_FILE, LIBRARY_TIMEZONE, MAX_NO_SHOWS

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
    """Loads booking data and sanitizes fields."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            try:
                data = json.load(f)
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
    Checks for expired bookings and No-Shows.
    If a user hits MAX_NO_SHOWS, applies a 14-day ban to their profile.
    """
    updated = False
    now = datetime.now(LIBRARY_TIMEZONE)
    
    # We need to track which users get a new No-Show to check their ban status
    users_to_check = set()

    for booking in bookings:
        current_status = booking.get('status', 'Confirmed')
        
        if current_status in ("Confirmed", "Active"):
            start_dt = LIBRARY_TIMEZONE.localize(datetime.strptime(f"{booking['date']} {booking['start_time']}", "%Y-%m-%d %H:%M"))
            end_dt = LIBRARY_TIMEZONE.localize(datetime.strptime(f"{booking['date']} {booking['end_time']}", "%Y-%m-%d %H:%M"))
            
            # 1. Check for No-Show (Start + 15mins passed)
            if current_status == "Confirmed":
                no_show_deadline = start_dt + timedelta(minutes=15)
                if now > no_show_deadline:
                    booking['status'] = "No-Show" 
                    updated = True
                    users_to_check.add(booking['user_email'])
            
            # 2. Check for Completion (End time passed)
            elif current_status == "Active":
                if now > end_dt:
                    booking['status'] = "Completed" 
                    updated = True
            
    if updated:
        save_data(bookings)
        
    # --- BAN ENFORCEMENT LOGIC ---
    if users_to_check:
        user_data = load_student_ids()
        ids_updated = False
        
        for email in users_to_check:
            # Count total no-shows for this user
            user_no_shows = sum(1 for b in bookings if b.get('user_email') == email and b.get('status') == 'No-Show')
            
            # If they hit the limit, set the ban date
            if user_no_shows >= MAX_NO_SHOWS:
                # Check if they are already banned to avoid resetting the timer
                current_profile = user_data.get(email, {})
                if 'ban_release_date' not in current_profile:
                    ban_end = now + timedelta(days=14)
                    user_data[email]['ban_release_date'] = ban_end.isoformat()
                    ids_updated = True
        
        if ids_updated:
            save_student_ids(user_data)

    return bookings

def get_eligible_bookings(all_bookings):
    """Returns bookings for the current user within check-in window."""
    eligible_bookings = []
    now_tz = datetime.now(LIBRARY_TIMEZONE)
    
    for booking in all_bookings:
        if booking.get('user_email') == st.session_state.user_email and booking.get('status', 'Confirmed') == 'Confirmed':
            start_dt = LIBRARY_TIMEZONE.localize(datetime.strptime(f"{booking['date']} {booking['start_time']}", "%Y-%m-%d %H:%M"))
            min_checkin = start_dt - timedelta(minutes=15)
            max_checkin = start_dt + timedelta(minutes=15)
            
            if min_checkin <= now_tz <= max_checkin:
                eligible_bookings.append(booking)
                
    return eligible_bookings