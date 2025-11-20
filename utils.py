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

# [QR CODE FUNCTION REMOVED HERE]

# ==========================================
# 📡 LIVE MAP SIMULATION LOGIC
# ==========================================

def get_target_occupancy(hour):
    # 1. Check JSON Sensor Data
    sensor_data = get_sensor_data()
    if sensor_data.get("manual_override", False):
        return float(sensor_data.get("target_occupancy", 0.5))

    # 2. Fallback to Bell Curve
    if hour < 8 or hour >= 20: return 0.0 
    peak_hour = 14
    max_occupancy = 0.85
    spread = 4 
    occupancy = max_occupancy * math.exp(-0.5 * ((hour - peak_hour) / spread) ** 2)
    return max(0.1, occupancy) 

def update_seat_simulation(current_states, all_seats):
    now_hour = get_current_time().hour 
    
    if now_hour >= 20 or now_hour < 8:
        return {seat_id: "Available" for seat_id in all_seats}

    target_occupancy = get_target_occupancy(now_hour)
    new_states = current_states.copy()
    
    if not new_states:
        for seat_id in all_seats:
            if random.random() < target_occupancy:
                new_states[seat_id] = "Occupied"
            else:
                new_states[seat_id] = "Available"
        return new_states

    for seat_id in all_seats:
        current_status = new_states.get(seat_id, "Available")
        
        if current_status == "Occupied":
            if random.random() < 0.05: new_states[seat_id] = "Available"
        else:
            current_total = sum(1 for s in new_states.values() if s == "Occupied")
            if (current_total / len(all_seats)) < target_occupancy:
                if random.random() < 0.10: new_states[seat_id] = "Occupied"
            else:
                if random.random() < 0.01: new_states[seat_id] = "Occupied"
                    
    return new_states