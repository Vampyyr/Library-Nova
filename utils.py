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
# 📡 LIVE MAP SIMULATION LOGIC (SYNCED)
# ==========================================

SEAT_DB = "seat_live_status.json"

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

def update_seat_simulation(ignored_current_states, all_seats):
    """
    Reads/Writes to a shared JSON file so all users see the same dots.
    Updates the simulation only if the data is 'stale' (older than 2 mins).
    """
    now = get_current_time()
    now_hour = now.hour
    
    # 1. Night/Early Morning Reset
    if now_hour >= 20 or now_hour < 8:
        return {seat_id: "Available" for seat_id in all_seats}

    # 2. Try to load shared state from file
    current_file_states = {}
    data_is_fresh = False
    
    if os.path.exists(SEAT_DB):
        try:
            with open(SEAT_DB, "r") as f:
                data = json.load(f)
                # Check if timestamp exists and calculate age
                if "timestamp" in data:
                    # Handle format compatibility if timestamp was saved differently previously
                    try:
                        last_update = datetime.fromisoformat(data["timestamp"])
                        # If data is less than 2 minutes old, use it without changing anything
                        # Note: This ensures User B sees what User A just generated.
                        if (now - last_update).total_seconds() < 5:
                            return data.get("seats", {})
                        else:
                            # Data exists but is old -> use it as the base for the next simulation step
                            current_file_states = data.get("seats", {})
                    except ValueError:
                        pass # Invalid timestamp format, regenerate
        except:
            pass # If file error, we just regenerate

    # 3. Run Simulation Logic (if fresh data wasn't returned)
    target_occupancy = get_target_occupancy(now_hour)
    new_states = current_file_states.copy()
    
    # Initialize if empty (First run of the day or file missing)
    if not new_states:
        for seat_id in all_seats:
            new_states[seat_id] = "Occupied" if random.random() < target_occupancy else "Available"
    else:
        # People arriving/leaving logic based on previous state
        current_total = sum(1 for s in new_states.values() if s == "Occupied")
        current_pct = current_total / len(all_seats) if len(all_seats) > 0 else 0

        for seat_id in all_seats:
            current_status = new_states.get(seat_id, "Available")
            
            if current_status == "Occupied":
                # Chance to leave (higher if over capacity)
                leave_prob = 0.05 if current_pct <= target_occupancy else 0.20
                if random.random() < leave_prob: 
                    new_states[seat_id] = "Available"
                    
            else:
                # Chance to sit (higher if under capacity)
                if current_pct < target_occupancy:
                    fill_prob = 0.15 if (target_occupancy - current_pct) > 0.1 else 0.05
                    if random.random() < fill_prob: 
                        new_states[seat_id] = "Occupied"
                else:
                    # Random noise (someone sits even if busy)
                    if random.random() < 0.005: 
                        new_states[seat_id] = "Occupied"

    # 4. Save the NEW state to the file (with timestamp)
    try:
        with open(SEAT_DB, "w") as f:
            json.dump({
                "timestamp": now.isoformat(),
                "seats": new_states
            }, f)
    except:
        pass # Prevent crash if write fails

    return new_states