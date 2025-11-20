import streamlit as st
import random
import string
import math
import os
import json
from datetime import datetime, timedelta
from config import LIBRARY_TIMEZONE

# ==========================================
# 🧪 TIME MACHINE & SENSORS
# ==========================================

def get_current_time():
    """Returns the current time, UNLESS 'time_machine.json' forces a specific time."""
    now = datetime.now(LIBRARY_TIMEZONE)
    
    # 1. Check JSON File (Backend override)
    if os.path.exists("time_machine.json"):
        try:
            with open("time_machine.json", "r") as f:
                data = json.load(f)
                if data.get("active", False):
                    target_hour = data.get("hour", now.hour)
                    target_minute = data.get("minute", now.minute)
                    return now.replace(hour=target_hour, minute=target_minute, second=0)
        except: pass

    # 2. Check Sidebar Slider (Frontend override)
    if 'dev_hour' in st.session_state:
        return now.replace(hour=st.session_state.dev_hour, minute=0, second=0)
    
    return now

def get_sensor_data():
    if os.path.exists("sensors.json"):
        try:
            with open("sensors.json", "r") as f:
                return json.load(f)
        except: return {}
    return {}

# ==========================================
# 🛠️ STANDARD UTILITIES
# ==========================================

def generate_checkin_code(length=3):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# ==========================================
# 📡 LIVE MAP SIMULATION LOGIC
# ==========================================

def get_target_occupancy(hour):
    """
    Returns the target occupancy percentage (0.0 to 1.0) based on the hour.
    Custom Logic:
    - Morning (8-11): Average (~60%)
    - Lunch (12-13): Low/Free (~35%)
    - Peak (15-18): High (90%+)
    - Closing (19+): Low (~30%)
    """
    # 1. Check JSON Sensor Data (Manual Override)
    sensor_data = get_sensor_data()
    if sensor_data.get("manual_override", False):
        return float(sensor_data.get("target_occupancy", 0.5))

    # 2. Define Hourly Distribution
    if hour < 8 or hour >= 20: return 0.0 

    # Map: Hour -> Occupancy %
    # Weighted to average ~65% across the open hours
    distribution = {
        8:  0.45, # Opening (Ramping up)
        9:  0.60, # Morning Average
        10: 0.65, # Morning Average
        11: 0.65, # Morning Average
        12: 0.40, # Lunch Dip (Pretty free)
        13: 0.35, # Lunch Dip (Pretty free)
        14: 0.55, # Post-lunch return
        15: 0.90, # Peak Start
        16: 0.98, # Peak High
        17: 0.92, # Peak Sustain
        18: 0.75, # Tapering off
        19: 0.30  # Closing soon
    }
    
    return distribution.get(hour, 0.5)

def update_seat_simulation(current_states, all_seats):
    now_hour = get_current_time().hour 
    
    if now_hour >= 20 or now_hour < 8:
        return {seat_id: "Available" for seat_id in all_seats}

    target_occupancy = get_target_occupancy(now_hour)
    new_states = current_states.copy()
    
    # Initialize if empty
    if not new_states:
        for seat_id in all_seats:
            if random.random() < target_occupancy:
                new_states[seat_id] = "Occupied"
            else:
                new_states[seat_id] = "Available"
        return new_states

    # Update states based on target occupancy
    for seat_id in all_seats:
        current_status = new_states.get(seat_id, "Available")
        
        if current_status == "Occupied":
            # If occupied, small chance to leave
            # (Chance increases if we are OVER our target occupancy)
            current_total = sum(1 for s in new_states.values() if s == "Occupied")
            current_pct = current_total / len(all_seats)
            
            leave_prob = 0.05 if current_pct <= target_occupancy else 0.20
            if random.random() < leave_prob: 
                new_states[seat_id] = "Available"
                
        else:
            # If available, calculate chance to sit
            current_total = sum(1 for s in new_states.values() if s == "Occupied")
            current_pct = current_total / len(all_seats)
            
            # Only fill seats if we are below target
            if current_pct < target_occupancy:
                # Higher chance to fill if we are far below target
                fill_prob = 0.15 if (target_occupancy - current_pct) > 0.1 else 0.05
                if random.random() < fill_prob: 
                    new_states[seat_id] = "Occupied"
            else:
                # Very small random noise
                if random.random() < 0.005: 
                    new_states[seat_id] = "Occupied"
                    
    return new_states