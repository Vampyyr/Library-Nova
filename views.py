import streamlit as st
import random
import time
import base64
import pandas as pd 
from datetime import datetime, timedelta, time as dt_time, date
from config import LIBRARY_TIMEZONE, FLOOR_PLANS, ALL_FREE_SEATS, AVAILABLE_RESOURCES, MAX_NO_SHOWS
# UPDATED IMPORT (Removed generate_qr_image):
from utils import generate_checkin_code, update_seat_simulation, get_target_occupancy, get_current_time
from auth import update_user_password, update_profile_picture
from data_manager import load_data, save_data, cleanup_and_update_bookings, get_eligible_bookings, load_student_ids

# ==========================================
# 🎨 STYLES & THEME
# ==========================================

def apply_custom_styles():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    [data-testid="collapsedControl"] {display: block;} 
    
    .stApp {
        background-color: #000000;
        color: #F5F5F7;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* INCREASE TAB FONT SIZE */
    div[data-baseweb="tab-list"] p {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #1C1C1E; 
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    div.stButton > button { 
        width: 100%;
        background-color: #2C2C2E !important;
        color: #FFFFFF !important; 
        border: none !important;
        border-radius: 12px !important; 
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover { 
        background-color: #3A3A3C !important; 
        transform: scale(1.01);
    }
    
    h1, h2, h3 { font-weight: 700 !important; letter-spacing: -0.02em !important; }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.8rem !important; }
    div[data-testid="stMetricLabel"] { color: #AEAEB2 !important; }
    
    .logo-container { position: absolute; top: -40px; left: -40px; z-index: 1000; }
    .logo-container img { height: 80px; width: auto; }
    
    .floor-plan-container { 
        position: relative; 
        width: 100%; max-width: 800px; 
        margin: 20px auto; 
        border-radius: 12px; overflow: hidden; 
        background-color: #FFFFFF; 
        border: 4px solid #1C1C1E; 
    }
    .floor-plan-container img { width: 100%; height: auto; display: block; object-fit: contain; }
    </style>
    """, unsafe_allow_html=True)

def render_logo_and_title():
    st.sidebar.header("🧪 Dev Tools")
    
    st.sidebar.caption("1. Time Machine")
    current_hour = datetime.now(LIBRARY_TIMEZONE).hour
    dev_hour = st.sidebar.slider("Simulate Hour", 0, 23, current_hour)
    st.session_state.dev_hour = dev_hour
    st.sidebar.write(f"🕒 **Simulated:** {dev_hour}:00")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("2. Quick Actions")
    
    if st.sidebar.button("⚡ Quick Book (Now)", type="primary"):
        all_bookings = load_data()
        now = get_current_time()
        code = generate_checkin_code()
        test_booking = {
            "user_email": st.session_state.get('user_email', 'test@novasbe.pt'),
            "type": "Group Study Room",
            "resource_id": "TEST-ROOM-01",
            "date": now.strftime("%Y-%m-%d"),
            "start_time": now.strftime("%H:%M"),
            "end_time": (now + timedelta(minutes=60)).strftime("%H:%M"),
            "duration": "60 minutes",
            "checkin_code": code,
            "status": "Confirmed",
            "check_in_time": None
        }
        all_bookings.append(test_booking)
        save_data(all_bookings)
        st.sidebar.success(f"Created! Code: {code}")
        time.sleep(1); st.rerun()

    if st.sidebar.button("🗑️ Reset All Bookings"):
        save_data([])
        st.sidebar.warning("Database wiped!")
        time.sleep(1); st.rerun()

    st.markdown("""<div class="logo-container"><img src="https://data.maglr.com/2991/issues/32619/420528/assets/css/img/C1b6d5df0ef776ed6767e958076af26b94e3d83ede7af31ada0a71e8c5166e61e.png" alt="NOVA SBE Logo"></div>""", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>Alexandre dos Santos Library</h1>", unsafe_allow_html=True)

# ==========================================
# 🏠 HOME TAB
# ==========================================

def render_home_tab():
    st.markdown('<img src="https://www.novasbe.unl.pt/Portals/0/Noticia%20Exposicao.jpg" style="width: 100%; border-radius: 16px; margin-top: 15px; opacity: 0.85;">', unsafe_allow_html=True)
    
    first_name = st.session_state.get('display_name', 'Student').split()[0]
    st.markdown(f"## 👋 Welcome back, {first_name}!")
    st.caption("Your central hub for study, research, and collaboration.")
    st.markdown("---")
    
    now = get_current_time()
    
    if st.session_state.get('library_override') == "CLOSED":
        status = "⛔ Emergency Close"
    else:
        status = "Open" if 8 <= now.hour < 20 else "Closed"
    
    if 'seat_states' not in st.session_state: st.session_state.seat_states = {}
    st.session_state.seat_states = update_seat_simulation(st.session_state.seat_states, ALL_FREE_SEATS.keys())
    
    total_seats = len(ALL_FREE_SEATS)
    occupied_seats = sum(1 for s in st.session_state.seat_states.values() if s == "Occupied")
    occupancy_pct = int((occupied_seats / total_seats) * 100) if total_seats > 0 else 0

    all_bookings = load_data()
    today_str = now.strftime("%Y-%m-%d")
    current_time = now.time()
    active_resources = set()
    
    for b in all_bookings:
        if b['date'] == today_str and b['status'] in ['Confirmed', 'Active']:
            start = datetime.strptime(b['start_time'], "%H:%M").time()
            end = datetime.strptime(b['end_time'], "%H:%M").time()
            if start <= current_time < end: 
                active_resources.add(b['resource_id'])
    
    free_rooms = max(0, len(AVAILABLE_RESOURCES["Group Study Room"]) - sum(1 for r in active_resources if "G-R" in r))
    free_bt = max(0, len(AVAILABLE_RESOURCES["Bloomberg Terminal"]) - sum(1 for r in active_resources if "BT" in r))

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Library Status", status)
    with col2: st.metric("Live Occupancy", f"{occupancy_pct}%")
    with col3: st.metric("Group Rooms", f"{free_rooms} Available")
    with col4: st.metric("Bloomberg", f"{free_bt} Available")
    
    st.markdown("---")
    st.markdown("### 📅 Campus Events")

    c1, c2, c3 = st.columns(3)
    events = [
        {"title": "Python for Finance", "date": "Oct 20", "time": "14:00", "loc": "Room B003", "img": "https://placehold.co/400x200/2C2C2E/FFFFFF?text=Python+Workshop"},
        {"title": "Alumni Network Talk", "date": "Nov 25", "time": "18:30", "loc": "Auditorium", "img": "https://placehold.co/400x200/2C2C2E/FFFFFF?text=Alumni+Talk"},
        {"title": "CV & Career Lab", "date": "Dec 01", "time": "10:00", "loc": "Room D-111", "img": "https://placehold.co/400x200/2C2C2E/FFFFFF?text=Career+Lab"},
    ]
    
    for col, evt in zip([c1, c2, c3], events):
        with col:
            with st.container(border=True):
                st.markdown(f"""
                <div style="height: 150px; width: 100%; overflow: hidden; border-radius: 8px; margin-bottom: 12px;">
                    <img src="{evt['img']}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**{evt['title']}**")
                st.caption(f"📅 {evt['date']} • {evt['time']}")
                st.caption(f"📍 {evt['loc']}")

# ==========================================
# 💡 LIVE MAP TAB
# ==========================================

def render_live_tab():
    st.markdown("<h2 style='text-align: center;'>Live Seat Availability</h2>", unsafe_allow_html=True)
    
    with st.expander("ℹ️ How this works", expanded=False):
        st.markdown("""
        **Free-Roaming Zone:**
        The dots below represent **general study seats**. These are **first-come, first-served** and cannot be booked.
        """)

    with st.expander("📊 View Typical Busy Hours", expanded=False):
        st.markdown("### Average Popularity by Hour")
        hours_range = range(8, 21)
        time_labels = [f"{h:02d}:00" for h in hours_range]
        occupancy_values = [int(get_target_occupancy(h) * 100) for h in hours_range]
        df_chart = pd.DataFrame({"Occupancy (%)": occupancy_values, "Time": time_labels}).set_index("Time")
        st.bar_chart(df_chart, color="#29B6F6") 
        st.caption("Based on historical traffic data (Gaussian Distribution).")

    st.markdown("---")

    now = get_current_time()
    if now.hour >= 20 or now.hour < 8:
        diff = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0) - now if now.hour >= 20 else now.replace(hour=8, minute=0, second=0) - now
        st.warning(f"🌙 **LIBRARY IS CLOSED** | Opens in {int(diff.total_seconds() // 3600)}h {int((diff.total_seconds() % 3600) // 60)}m")

    if 'seat_states' not in st.session_state: st.session_state.seat_states = {}
    if 'current_floor' not in st.session_state: st.session_state.current_floor = "Second Floor" 

    with st.container(border=True):
        c1, c2, c_spacer, c3 = st.columns([1, 1, 0.5, 1])
        with c1: 
            if st.button("First Floor", key="btn_f1"): st.session_state.current_floor = "First Floor"
        with c2: 
            if st.button("Second Floor", key="btn_f2"): st.session_state.current_floor = "Second Floor"
        with c3:
            st.markdown('<div style="margin-top: 5px;"></div>', unsafe_allow_html=True)
            live_mode = st.toggle("Auto-Refresh", value=False)

    st.markdown("---")

    st.session_state.seat_states = update_seat_simulation(st.session_state.seat_states, ALL_FREE_SEATS.keys())
    current_floor = st.session_state.current_floor
    current_floor_seats = {sid: data for sid, data in ALL_FREE_SEATS.items() if data["floor"] == current_floor}
    
    html_dots = ""
    visible_statuses = {}
    for seat_id, dot_info in current_floor_seats.items():
        status = st.session_state.seat_states.get(seat_id, "Available")
        color = "#30D158" if status == "Available" else "#FF453A" 
        visible_statuses[seat_id] = status
        html_dots += f'<div style="position: absolute; top: {dot_info["y"]}; left: {dot_info["x"]}; width: 10px; height: 10px; background-color: {color}; border-radius: 50%; box-shadow: 0 0 3px rgba(0, 0, 0, 0.5); z-index: 2000; transition: background-color 0.5s ease;"></div>'

    avail_count = sum(1 for s in visible_statuses.values() if s == 'Available')
    
    c_left, c_right = st.columns([2, 1])
    with c_left: st.markdown(f"### {current_floor}")
    with c_right: st.markdown(f"<div style='text-align:right; font-size:1.5em; font-weight:700; color:#30D158;'>{avail_count} <span style='font-size:0.6em; color:#8E8E93;'>/ {len(visible_statuses)} Available</span></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="floor-plan-container">
        <img src="{FLOOR_PLANS[current_floor]}" alt="{current_floor} Floor Plan">
        {html_dots}
    </div>
    """, unsafe_allow_html=True)

    if live_mode:
        time.sleep(3)
        st.rerun()

# ==========================================
# 📅 BOOKING LOGIC & TAB
# ==========================================

def handle_booking_submission(all_bookings, selected_date, selected_time_str, duration, booking_type):
    if selected_time_str is None or selected_time_str == "No slots available" or duration == 0:
         st.error("Booking failed: No valid time selected.")
         return

    target_date_str = selected_date.strftime("%Y-%m-%d")
    start_time_dt = datetime.strptime(selected_time_str, "%H:%M").time()
    
    user_bookings = [b for b in all_bookings if b['user_email'] == st.session_state.user_email]
    if sum(1 for b in user_bookings if b.get('status', 'Confirmed') == 'No-Show') >= MAX_NO_SHOWS:
        st.error(f"Booking blocked: You have reached the No-Show limit ({MAX_NO_SHOWS}).")
        return

    user_bookings_today = [b for b in user_bookings if b['date'] == target_date_str and b.get('status', 'Confirmed') in ("Confirmed", "Active")]
    if len(user_bookings_today) >= 2:
        st.error("Booking failed: Limit of 2 bookings per day reached.")
        return

    start_dt = datetime.combine(selected_date, start_time_dt) 
    end_dt = start_dt + timedelta(minutes=duration)
    
    all_ids = [r['id'] for r in AVAILABLE_RESOURCES.get(booking_type, [])]
    booked_ids = set()
    
    for b in all_bookings:
        if b['date'] == target_date_str and b.get('status', 'Confirmed') in ("Confirmed", "Active"): 
            ex_start = datetime.strptime(b['start_time'], "%H:%M")
            ex_end = datetime.strptime(b['end_time'], "%H:%M")
            ex_start = datetime.combine(selected_date, ex_start.time())
            ex_end = datetime.combine(selected_date, ex_end.time())
            if (end_dt > ex_start) and (ex_end > start_dt):
                if b['resource_id'] in all_ids: 
                    booked_ids.add(b['resource_id'])

    available = [rid for rid in all_ids if rid not in booked_ids]
    
    if not available:
        st.error(f"No slots available for the selected time.")
        return

    res_id = random.choice(available)
    code = generate_checkin_code()
    new_booking = {
        "user_email": st.session_state.user_email, 
        "type": booking_type, 
        "resource_id": res_id, 
        "date": target_date_str, 
        "start_time": start_dt.strftime("%H:%M"), 
        "end_time": end_dt.strftime("%H:%M"), 
        "duration": f"{duration} minutes", 
        "checkin_code": code, 
        "status": "Confirmed", 
        "check_in_time": None
    }
    all_bookings.append(new_booking)
    save_data(all_bookings)
    st.success(f"Booking confirmed for {res_id} on {selected_date}!")
    st.markdown(f"**Check-in Code:** <span style='font-size: 1.5em; color: #FFD60A;'>**{code}**</span>", unsafe_allow_html=True)
    time.sleep(2) 
    st.rerun()

def render_bookings_tab():
    st.markdown("<h2 style='text-align: center;'>Book a Slot</h2>", unsafe_allow_html=True)
    
    all_bookings = load_data()
    all_bookings = cleanup_and_update_bookings(all_bookings)
    
    current_eligible = get_eligible_bookings(all_bookings)
    if current_eligible:
        with st.container(border=True):
            st.info(f"⚡ **Ready to Check In!** ({len(current_eligible)} bookings)")
            c1, c2 = st.columns([3, 1])
            with c1: 
                code = st.text_input("Enter 3-Letter Code:", max_chars=3, label_visibility="collapsed", placeholder="Type Code").upper().strip()
            with c2: 
                if st.button("Check In", type="primary"):
                    for b in current_eligible:
                        if b.get('checkin_code') == code and b['user_email'] == st.session_state.user_email:
                            b['status'] = "Active"
                            b['check_in_time'] = datetime.now(LIBRARY_TIMEZONE).strftime("%Y-%m-%d %H:%M")
                            save_data(all_bookings)
                            st.success("Checked in!"); st.rerun()
                    st.error("Invalid code.")
    
    with st.container(border=True):
        st.markdown("#### 📅 New Booking")
        if sum(1 for b in all_bookings if b['user_email'] == st.session_state.user_email and b.get('status') == 'No-Show') >= MAX_NO_SHOWS:
            st.error("⚠️ BOOKING BLOCKED: Too many No-Shows. Contact Admin.")
        else:
            c1, c2 = st.columns(2)
            with c1: b_type = st.selectbox("Resource:", list(AVAILABLE_RESOURCES.keys()))
            with c2: sel_date = st.date_input("Date:", min_value=date.today(), max_value=date.today()+timedelta(days=7), value=date.today())
            
            now_tz = get_current_time()
            today_tz = now_tz.date()
            all_slots = [f"{h:02d}:{m:02d}" for h in range(8, 20) for m in (0, 30)]
            
            avail_times = []
            if sel_date > today_tz: 
                avail_times = all_slots 
            elif sel_date == today_tz:
                cur_mins = now_tz.hour * 60 + now_tz.minute
                for s in all_slots:
                    h, m = map(int, s.split(':'))
                    if (h * 60 + m) > cur_mins: avail_times.append(s)
            
            display_options = avail_times if avail_times else ["No slots available"]
            
            c3, c4 = st.columns(2)
            with c3: sel_time_str = st.selectbox("Start Time:", display_options, key=f"time_{sel_date}")
            with c4:
                duration = 0
                if sel_time_str and sel_time_str != "No slots available":
                    start_dt = datetime.combine(sel_date, datetime.strptime(sel_time_str, "%H:%M").time())
                    rem_mins = int((datetime.combine(sel_date, dt_time(20,0)) - start_dt).total_seconds()/60)
                    max_dur = (min(120, rem_mins) // 30) * 30
                    if max_dur >= 30:
                        dur_opts = [m for m in [30, 60, 90, 120] if m <= max_dur]
                        duration = st.selectbox("Duration:", dur_opts, format_func=lambda x: f"{x} mins", key=f"dur_{sel_date}_{sel_time_str}")
                    else: st.selectbox("Duration:", ["N/A"], disabled=True)
                else: st.selectbox("Duration:", ["N/A"], disabled=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Confirm Booking", type="primary"):
                handle_booking_submission(all_bookings, sel_date, sel_time_str, duration, b_type)

    st.markdown("### Your Bookings")
    my_bookings = [b for b in all_bookings if b.get('user_email') == st.session_state.user_email]
    
    if 'cancel_code' not in st.session_state: st.session_state.cancel_code = None
    if st.session_state.cancel_code:
        save_data([b for b in all_bookings if b['checkin_code'] != st.session_state.cancel_code])
        st.session_state.cancel_code = None; st.rerun()

    if not my_bookings:
        st.info("You have no upcoming bookings.")
    else:
        for b in sorted(my_bookings, key=lambda x: x['date']):
            status = b.get('status', 'Confirmed')
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                badge = f'<span class="status-badge status-{status.replace(" ", "-")}">{status.upper()}</span>'
                with c1: 
                    st.markdown(f"**{b['type']}** | {b['date']}")
                    st.caption(f"Resource: {b['resource_id']} | Time: {b['start_time']} - {b['end_time']}")
                    st.markdown(f"**Check-in Code:** <span style='font-size:1.2em; color:#FFD60A; background:#333; padding:2px 6px; border-radius:4px;'>{b['checkin_code']}</span> {badge}", unsafe_allow_html=True)
                with c2:
                    # QR POPUP REMOVED HERE to fix ModuleNotFoundError
                    st.empty()
                with c3:
                    if status == "Confirmed": 
                        if st.button("Cancel", key=f"c_{b['checkin_code']}", use_container_width=True):
                            st.session_state.update(cancel_code=b['checkin_code'])

# ==========================================
# 👤 PROFILE TAB
# ==========================================

def render_profile_tab():
    st.markdown("<h2 style='text-align: center;'>My Profile</h2>", unsafe_allow_html=True)
    
    user_data_all = load_student_ids()
    current_user_data = user_data_all.get(st.session_state.user_email, {})
    custom_pic_b64 = current_user_data.get('profile_pic', None)

    with st.container(border=True):
        c1, c2 = st.columns([1, 3])
        with c1:
            if custom_pic_b64:
                try:
                    img_bytes = base64.b64decode(custom_pic_b64)
                    st.image(img_bytes, width=100)
                except: st.error("Error loading image")
            else:
                initials = "".join([n[0] for n in st.session_state.display_name.split() if n]).upper()
                st.image(f"https://placehold.co/120x120/2C2C2E/FFFFFF?text={initials}", width=100)
        with c2:
            st.markdown(f"### {st.session_state.display_name}")
            st.markdown(f"**ID:** `{st.session_state.student_number}`")
            st.caption(f"{st.session_state.user_email} • {st.session_state.user_role}")

    all_bookings = load_data()
    my_bookings = [b for b in all_bookings if b.get('user_email') == st.session_state.user_email]
    no_shows = sum(1 for b in my_bookings if b.get('status') == 'No-Show')
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        with st.container(border=True): st.metric("Total Bookings", len(my_bookings))
    with c2:
        with st.container(border=True): st.metric("Active Now", sum(1 for b in my_bookings if b.get('status') == 'Active'))
    with c3:
        with st.container(border=True): st.metric("No-Shows", f"{no_shows}/{MAX_NO_SHOWS}")
    
    if no_shows >= MAX_NO_SHOWS: st.error("🚫 You are currently restricted from booking due to No-Shows.")

    st.markdown("### Settings")
    with st.container(border=True):
        with st.expander("📸 Change Profile Picture"):
            uploaded_file = st.file_uploader("Upload a new photo", type=['png', 'jpg', 'jpeg'])
            if uploaded_file is not None:
                if st.button("Save Photo", type="primary"):
                    if update_profile_picture(st.session_state.user_email, uploaded_file):
                        st.success("Updated!"); time.sleep(1); st.rerun()
                    else: st.error("Failed to save.")

        with st.expander("🔒 Change Password"):
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm New Password", type="password")
            if st.button("Update Password"):
                if len(new_pass) < 1: st.error("Cannot be empty.")
                elif new_pass != confirm_pass: st.error("Passwords do not match.")
                else: 
                    if update_user_password(st.session_state.user_email, new_pass): st.success("Updated!")
                    else: st.error("Failed.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Log Out", type="primary", use_container_width=True):
            st.session_state.logged_in = False; st.rerun()

# ==========================================
# 👮 ADMIN DASHBOARD TAB
# ==========================================

def render_admin_tab():
    c_title, c_logout = st.columns([5, 1])
    with c_title: st.markdown("## Librarian Dashboard")
    with c_logout: 
        if st.button("Log Out", key="admin_logout", type="primary"):
            st.session_state.logged_in = False; st.rerun()
            
    all_bookings = load_data()
    all_bookings = cleanup_and_update_bookings(all_bookings)
    
    now = get_current_time()
    today_str = now.strftime("%Y-%m-%d")
    todays_bookings = [b for b in all_bookings if b['date'] == today_str and b['status'] in ('Confirmed', 'Active')]
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Bookings Today", len(todays_bookings))
    col2.metric("Active Now", sum(1 for b in todays_bookings if b['status'] == 'Active'))
    col3.metric("Total No-Shows", sum(1 for b in all_bookings if b['status'] == 'No-Show'))

    st.markdown("---"); st.subheader("🚨 Emergency Controls")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Force Close Library", type="primary"):
            st.session_state.library_override = "CLOSED"
            st.success("Library marked as CLOSED.")
            time.sleep(1); st.rerun()
    with c2:
        if st.button("Reset to Normal Hours"):
            st.session_state.library_override = None
            st.success("Schedule reset.")
            time.sleep(1); st.rerun()
    
    st.markdown("---"); st.subheader("🔎 Student Lookup & Penalty Reset")
    search_email = st.text_input("Enter Student Email:", placeholder="e.g. 55443@novasbe.pt")
    
    if search_email:
        student_bookings = [b for b in all_bookings if b['user_email'] == search_email]
        if not student_bookings: st.warning("No booking history found for this email.")
        else:
            no_shows = sum(1 for b in student_bookings if b['status'] == 'No-Show')
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**No-Shows:** {no_shows} / {MAX_NO_SHOWS}")
                if no_shows >= MAX_NO_SHOWS: st.error("🚫 BLOCKED")
                else: st.success("✅ Good Standing")
            with c2:
                if no_shows > 0:
                    if st.button("Forgive All", type="primary"):
                        for b in all_bookings:
                            if b['user_email'] == search_email and b['status'] == 'No-Show': 
                                b['status'] = 'Forgiven'
                        save_data(all_bookings); st.success("Forgiven!"); time.sleep(1); st.rerun()
    
    st.markdown("---"); st.subheader("📅 Master Booking List (Today)")
    if not todays_bookings: st.info("No bookings today.")
    else:
        for b in sorted(todays_bookings, key=lambda x: x['start_time']):
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
                with c1: st.markdown(f"**{b['resource_id']}**")
                with c2: st.markdown(f"{b['start_time']} - {b['end_time']}")
                with c3: st.markdown(f"`{b['user_email']}`")
                with c4:
                    if st.button("Force Cancel", key=f"admin_cancel_{b['checkin_code']}"):
                        all_bookings = [x for x in all_bookings if x['checkin_code'] != b['checkin_code']]
                        save_data(all_bookings); st.warning("Cancelled"); time.sleep(1); st.rerun()