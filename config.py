import pytz

# ==========================================
# ⚙️ CONFIGURATION & CONSTANTS
# ==========================================

# Set the library's local time zone (Lisbon/Portugal)
LIBRARY_TIMEZONE = pytz.timezone('Europe/Lisbon') 
DB_FILE = "bookings_db.json"
STUDENT_DB_FILE = "student_ids.json" 
MAX_NO_SHOWS = 3

CUSTOM_ICON_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXQWrqDJqabrGCzctITeYxl-gEAt4vXP5qgQ&s"
ADMIN_EMAIL = "admin@novasbe.pt"

# --- PORTUGUESE NAMES FOR MOCK PROFILES ---
PORTUGUESE_FIRST_NAMES = ["João", "Diogo", "Luís", "Miguel", "Pedro", "Francisco", "Afonso", "Maria", "Ana", "Beatriz", "Sofia", "Mariana", "Inês", "Leonor"]
PORTUGUESE_SURNAMES = ["Santos", "Silva", "Ferreira", "Sousa", "Pereira", "Oliveira", "Rodrigues", "Martins", "Gomes", "Fernandes"]

# --- GLOBAL RESOURCE DEFINITIONS ---
FLOOR_PLANS = {
    "First Floor": "https://i.imgur.com/Yx6yrhe.png", 
    "Second Floor": "https://i.imgur.com/FRYqx5w.png", 
}

AVAILABLE_RESOURCES = {
    "Group Study Room": [
        {"id": f"G-R{i:02d} (F1)"} for i in range(1, 5) 
    ] + [
        {"id": f"G-R{i:02d} (F2)"} for i in range(5, 9)
    ],
    "Bloomberg Terminal": [
        {"id": f"BT-{chr(65+i)} (F1)"} for i in range(8)
    ],
    "PC": [
        {"id": f"PC-{i:02d} (F2)"} for i in range(1, 23)
    ],
}

# ==========================================
# 🗺️ SEAT COORDINATES
# ==========================================

# ⚠️ IMPORTANT: Open your original library.py and copy the entire
# ALL_FREE_SEATS dictionary (approx lines 45-260) and paste it here.
# It should look like:
# ALL_FREE_SEATS = {
#    "1.01": {"floor": "First Floor","x": "76.6%", "y": "96.5%", "type": "Seat"},
#    ... (rest of the coordinates) ...
# }

ALL_FREE_SEATS = {
# ==========================================================================
    # FIRST FLOOR (F1) - Seats 1.01 to 1.32
    # ==========================================================================
    
    "1.01": {"floor": "First Floor","x": "76.6%", "y": "96.5%", "type": "Seat"},
    "1.02": {"floor": "First Floor", "x": "76.7%", "y": "94.3%", "type": "Seat"},
    "1.03": {"floor": "First Floor", "x": "70.5%", "y": "96.5%", "type": "Seat"},
    "1.04": {"floor": "First Floor", "x": "70.3%", "y": "94.3%", "type": "Seat"},
    "1.05": {"floor": "First Floor", "x": "66.3%", "y": "96.5%", "type": "Seat"},
    "1.06": {"floor": "First Floor", "x": "66.7%", "y": "94.3%", "type": "Seat"},
    "1.07": {"floor": "First Floor", "x": "60.7%", "y": "96.4%", "type": "Seat"},
    "1.08": {"floor": "First Floor", "x": "60.3%", "y": "94.3%", "type": "Seat"},
    "1.09": {"floor": "First Floor", "x": "56.4%", "y": "96.5%", "type": "Seat"},
    "1.10": {"floor": "First Floor", "x": "56.4%", "y": "94.3%", "type": "Seat"},
    "1.11": {"floor": "First Floor", "x": "50.5%", "y": "96.5%", "type": "Seat"},
    "1.12": {"floor": "First Floor", "x": "50.5%", "y": "94.4%", "type": "Seat"},
    "1.13": {"floor": "First Floor", "x": "42.6%", "y": "96.4%", "type": "Seat"},
    "1.14": {"floor": "First Floor", "x": "42.5%", "y": "94.3%", "type": "Seat"},
    "1.15": {"floor": "First Floor", "x": "36.4%", "y": "96.5%", "type": "Seat"},
    "1.16": {"floor": "First Floor", "x": "36.6%", "y": "94.3%", "type": "Seat"},
    "1.17": {"floor": "First Floor", "x": "32.5%", "y": "96.4%", "type": "Seat"},
    "1.18": {"floor": "First Floor", "x": "32.7%", "y": "94.3%", "type": "Seat"},
    "1.19": {"floor": "First Floor", "x": "26.6%", "y": "96.5%", "type": "Seat"},
    "1.20": {"floor": "First Floor", "x": "26.6%", "y": "94.3%", "type": "Seat"},
    "1.21": {"floor": "First Floor", "x": "23.2%", "y": "96.6%", "type": "Seat"},
    "1.22": {"floor": "First Floor", "x": "22.7%", "y": "94.3%", "type": "Seat"},
    "1.23": {"floor": "First Floor", "x": "16.6%", "y": "96.6%", "type": "Seat"},
    "1.24": {"floor": "First Floor", "x": "16.6%", "y": "94.3%", "type": "Seat"},
    "1.25": {"floor": "First Floor", "x": "22.7%", "y": "92.2%", "type": "Seat"},
    "1.26": {"floor": "First Floor", "x": "22.7%", "y": "90.0%", "type": "Seat"},
    "1.27": {"floor": "First Floor", "x": "16.4%", "y": "92.3%", "type": "Seat"},
    "1.28": {"floor": "First Floor", "x": "16.7%", "y": "90.1%", "type": "Seat"},
    "1.29": {"floor": "First Floor", "x": "23.0%", "y": "85.3%", "type": "Seat"},
    "1.30": {"floor": "First Floor", "x": "22.9%", "y": "82.9%", "type": "Seat"},
    "1.31": {"floor": "First Floor", "x": "16.6%", "y": "85.2%", "type": "Seat"},
    "1.32": {"floor": "First Floor", "x": "16.6%", "y": "83.0%", "type": "Seat"},

    # ==========================================================================
    # SECOND FLOOR (F2)
    # ==========================================================================
    
    "2.001": {"floor": "Second Floor", "x": "63.9%", "y": "95.1%", "type": "Seat"},
    "2.002": {"floor": "Second Floor", "x": "63.9%", "y": "92.4%", "type": "Seat"},
    "2.003": {"floor": "Second Floor", "x": "61.9%", "y": "95.1%", "type": "Seat"},
    "2.004": {"floor": "Second Floor", "x": "61.8%", "y": "92.4%", "type": "Seat"},
    "2.005": {"floor": "Second Floor", "x": "60.1%", "y": "95.2%", "type": "Seat"},
    "2.006": {"floor": "Second Floor", "x": "60.0%", "y": "92.0%", "type": "Seat"},
    "2.007": {"floor": "Second Floor", "x": "58.3%", "y": "95.1%", "type": "Seat"},
    "2.008": {"floor": "Second Floor", "x": "58.1%", "y": "92.1%", "type": "Seat"},
    "2.009": {"floor": "Second Floor", "x": "52.2%", "y": "95.0%", "type": "Seat"},
    "2.010": {"floor": "Second Floor", "x": "52.4%", "y": "92.2%", "type": "Seat"},
    "2.011": {"floor": "Second Floor", "x": "50.3%", "y": "94.9%", "type": "Seat"},
    "2.012": {"floor": "Second Floor", "x": "50.4%", "y": "91.9%", "type": "Seat"},
    "2.013": {"floor": "Second Floor", "x": "48.3%", "y": "94.9%", "type": "Seat"},
    "2.014": {"floor": "Second Floor", "x": "48.6%", "y": "92.1%", "type": "Seat"},
    "2.015": {"floor": "Second Floor", "x": "46.5%", "y": "95.1%", "type": "Seat"},
    "2.016": {"floor": "Second Floor", "x": "46.7%", "y": "92.1%", "type": "Seat"},
    "2.017": {"floor": "Second Floor", "x": "39.2%", "y": "95.5%", "type": "Seat"},
    "2.018": {"floor": "Second Floor", "x": "39.2%", "y": "92.3%", "type": "Seat"},
    "2.019": {"floor": "Second Floor", "x": "37.5%", "y": "95.2%", "type": "Seat"},
    "2.020": {"floor": "Second Floor", "x": "37.4%", "y": "92.1%", "type": "Seat"},
    "2.021": {"floor": "Second Floor", "x": "34.9%", "y": "95.4%", "type": "Seat"},
    "2.022": {"floor": "Second Floor", "x": "34.9%", "y": "92.2%", "type": "Seat"},
    "2.023": {"floor": "Second Floor", "x": "33.2%", "y": "95.4%", "type": "Seat"},
    "2.024": {"floor": "Second Floor", "x": "33.2%", "y": "92.4%", "type": "Seat"},
    "2.025": {"floor": "Second Floor", "x": "39.2%", "y": "88.9%", "type": "Seat"},
    "2.026": {"floor": "Second Floor", "x": "39.2%", "y": "85.7%", "type": "Seat"},
    "2.027": {"floor": "Second Floor", "x": "37.5%", "y": "88.9%", "type": "Seat"},
    "2.028": {"floor": "Second Floor", "x": "37.5%", "y": "85.7%", "type": "Seat"},
    "2.029": {"floor": "Second Floor", "x": "34.8%", "y": "88.9%", "type": "Seat"},
    "2.030": {"floor": "Second Floor", "x": "34.8%", "y": "85.7%", "type": "Seat"},
    "2.031": {"floor": "Second Floor", "x": "33.2%", "y": "88.8%", "type": "Seat"},
    "2.032": {"floor": "Second Floor", "x": "32.9%", "y": "85.7%", "type": "Seat"},
    "2.033": {"floor": "Second Floor", "x": "33.3%", "y": "80.7%", "type": "Seat"},
    "2.034": {"floor": "Second Floor", "x": "35.2%", "y": "80.7%", "type": "Seat"},
    "2.035": {"floor": "Second Floor", "x": "36.9%", "y": "80.5%", "type": "Seat"},
    "2.036": {"floor": "Second Floor", "x": "38.5%", "y": "80.5%", "type": "Seat"},
    "2.037": {"floor": "Second Floor", "x": "40.3%", "y": "80.5%", "type": "Seat"},
    "2.038": {"floor": "Second Floor", "x": "41.6%", "y": "79.1%", "type": "Seat"},
    "2.039": {"floor": "Second Floor", "x": "41.7%", "y": "77.4%", "type": "Seat"},
    "2.040": {"floor": "Second Floor", "x": "41.7%", "y": "75.8%", "type": "Seat"},
    "2.041": {"floor": "Second Floor", "x": "41.9%", "y": "74.1%", "type": "Seat"},
    "2.042": {"floor": "Second Floor", "x": "41.9%", "y": "72.6%", "type": "Seat"},
    "2.043": {"floor": "Second Floor", "x": "41.9%", "y": "70.8%", "type": "Seat"},
    "2.044": {"floor": "Second Floor", "x": "41.9%", "y": "69.2%", "type": "Seat"},
    "2.045": {"floor": "Second Floor", "x": "41.9%", "y": "67.6%", "type": "Seat"},
    "2.046": {"floor": "Second Floor", "x": "41.9%", "y": "66.0%", "type": "Seat"},
    "2.047": {"floor": "Second Floor", "x": "41.9%", "y": "64.3%", "type": "Seat"},
    "2.048": {"floor": "Second Floor", "x": "42.0%", "y": "62.4%", "type": "Seat"},
    "2.049": {"floor": "Second Floor", "x": "41.9%", "y": "60.8%", "type": "Seat"},
    "2.050": {"floor": "Second Floor", "x": "41.9%", "y": "59.4%", "type": "Seat"},
    "2.051": {"floor": "Second Floor", "x": "42.0%", "y": "57.6%", "type": "Seat"},
    "2.052": {"floor": "Second Floor", "x": "41.9%", "y": "56.0%", "type": "Seat"},
    "2.053": {"floor": "Second Floor", "x": "41.9%", "y": "54.4%", "type": "Seat"},
    "2.054": {"floor": "Second Floor", "x": "41.9%", "y": "52.6%", "type": "Seat"},
    "2.055": {"floor": "Second Floor", "x": "41.7%", "y": "50.8%", "type": "Seat"},
    "2.056": {"floor": "Second Floor", "x": "40.6%", "y": "48.0%", "type": "Seat"},
    "2.057": {"floor": "Second Floor", "x": "38.7%", "y": "47.3%", "type": "Seat"},
    "2.058": {"floor": "Second Floor", "x": "37.1%", "y": "47.0%", "type": "Seat"},
    "2.059": {"floor": "Second Floor", "x": "35.6%", "y": "46.7%", "type": "Seat"},
    "2.060": {"floor": "Second Floor", "x": "33.9%", "y": "46.3%", "type": "Seat"},

    "2.061": {"floor": "Second Floor", "x": "46.7%", "y": "69.2%", "type": "Seat"},
    "2.062": {"floor": "Second Floor", "x": "46.6%", "y": "72.3%", "type": "Seat"},
    "2.063": {"floor": "Second Floor", "x": "48.4%", "y": "69.1%", "type": "Seat"},
    "2.064": {"floor": "Second Floor", "x": "48.3%", "y": "72.3%", "type": "Seat"},
    "2.065": {"floor": "Second Floor", "x": "50.7%", "y": "69.0%", "type": "Seat"},
    "2.066": {"floor": "Second Floor", "x": "50.5%", "y": "72.2%", "type": "Seat"},
    "2.067": {"floor": "Second Floor", "x": "52.2%", "y": "68.8%", "type": "Seat"},
    "2.068": {"floor": "Second Floor", "x": "52.4%", "y": "72.1%", "type": "Seat"},
    "2.069": {"floor": "Second Floor", "x": "58.4%", "y": "69.0%", "type": "Seat"},
    "2.070": {"floor": "Second Floor", "x": "58.3%", "y": "72.4%", "type": "Seat"},
    "2.071": {"floor": "Second Floor", "x": "60.1%", "y": "69.1%", "type": "Seat"},
    "2.072": {"floor": "Second Floor", "x": "60.1%", "y": "72.3%", "type": "Seat"},
    "2.073": {"floor": "Second Floor", "x": "62.3%", "y": "68.9%", "type": "Seat"},
    "2.074": {"floor": "Second Floor", "x": "62.2%", "y": "72.3%", "type": "Seat"},
    "2.075": {"floor": "Second Floor", "x": "63.8%", "y": "68.8%", "type": "Seat"},
    "2.076": {"floor": "Second Floor", "x": "63.9%", "y": "72.4%", "type": "Seat"},

    "2.077": {"floor": "Second Floor", "x": "46.6%", "y": "54.0%", "type": "Seat"},
    "2.078": {"floor": "Second Floor", "x": "46.7%", "y": "57.2%", "type": "Seat"},
    "2.079": {"floor": "Second Floor", "x": "48.3%", "y": "53.9%", "type": "Seat"},
    "2.080": {"floor": "Second Floor", "x": "48.6%", "y": "57.2%", "type": "Seat"},
    "2.081": {"floor": "Second Floor", "x": "50.8%", "y": "53.9%", "type": "Seat"},
    "2.082": {"floor": "Second Floor", "x": "50.7%", "y": "56.9%", "type": "Seat"},
    "2.083": {"floor": "Second Floor", "x": "52.6%", "y": "53.9%", "type": "Seat"},
    "2.084": {"floor": "Second Floor", "x": "52.5%", "y": "57.2%", "type": "Seat"},
    "2.085": {"floor": "Second Floor", "x": "58.3%", "y": "53.9%", "type": "Seat"},
    "2.086": {"floor": "Second Floor", "x": "58.4%", "y": "57.2%", "type": "Seat"},
    "2.087": {"floor": "Second Floor", "x": "60.0%", "y": "53.7%", "type": "Seat"},
    "2.088": {"floor": "Second Floor", "x": "60.0%", "y": "57.2%", "type": "Seat"},
    "2.089": {"floor": "Second Floor", "x": "62.2%", "y": "53.7%", "type": "Seat"},
    "2.090": {"floor": "Second Floor", "x": "62.3%", "y": "57.2%", "type": "Seat"},
    "2.091": {"floor": "Second Floor", "x": "64.0%", "y": "53.9%", "type": "Seat"},
    "2.092": {"floor": "Second Floor", "x": "64.0%", "y": "57.0%", "type": "Seat"},

    "2.093": {"floor": "Second Floor", "x": "46.9%", "y": "46.6%", "type": "Seat"},
    "2.094": {"floor": "Second Floor", "x": "46.7%", "y": "50.1%", "type": "Seat"},
    "2.095": {"floor": "Second Floor", "x": "48.7%", "y": "46.4%", "type": "Seat"},
    "2.096": {"floor": "Second Floor", "x": "48.4%", "y": "50.0%", "type": "Seat"},
    "2.097": {"floor": "Second Floor", "x": "50.7%", "y": "46.6%", "type": "Seat"},
    "2.098": {"floor": "Second Floor", "x": "50.7%", "y": "49.9%", "type": "Seat"},
    "2.099": {"floor": "Second Floor", "x": "52.5%", "y": "46.7%", "type": "Seat"},
    "2.100": {"floor": "Second Floor", "x": "52.2%", "y": "50.0%", "type": "Seat"},
    "2.101": {"floor": "Second Floor", "x": "58.3%", "y": "46.9%", "type": "Seat"},
    "2.102": {"floor": "Second Floor", "x": "58.3%", "y": "50.0%", "type": "Seat"},
    "2.103": {"floor": "Second Floor", "x": "60.1%", "y": "46.7%", "type": "Seat"},
    "2.104": {"floor": "Second Floor", "x": "60.1%", "y": "50.0%", "type": "Seat"},
    "2.105": {"floor": "Second Floor", "x": "62.3%", "y": "46.7%", "type": "Seat"},
    "2.106": {"floor": "Second Floor", "x": "62.3%", "y": "50.3%", "type": "Seat"},
    "2.107": {"floor": "Second Floor", "x": "64.2%", "y": "46.7%", "type": "Seat"},
    "2.108": {"floor": "Second Floor", "x": "64.0%", "y": "50.2%", "type": "Seat"},

    "2.109": {"floor": "Second Floor", "x": "69.0%", "y": "46.3%", "type": "Seat"},
    "2.110": {"floor": "Second Floor", "x": "69.0%", "y": "50.4%", "type": "Seat"},
    "2.111": {"floor": "Second Floor", "x": "70.6%", "y": "46.2%", "type": "Seat"},
    "2.112": {"floor": "Second Floor", "x": "70.7%", "y": "50.4%", "type": "Seat"},
    "2.113": {"floor": "Second Floor", "x": "81.9%", "y": "51.0%", "type": "Seat"},
    "2.114": {"floor": "Second Floor", "x": "81.1%", "y": "54.1%", "type": "Seat"},
    "2.115": {"floor": "Second Floor", "x": "83.5%", "y": "51.5%", "type": "Seat"},
    "2.116": {"floor": "Second Floor", "x": "82.8%", "y": "54.4%", "type": "Seat"},

    "2.117": {"floor": "Second Floor", "x": "83.1%", "y": "44.5%", "type": "Seat"},
    "2.118": {"floor": "Second Floor", "x": "82.4%", "y": "47.6%", "type": "Seat"},
    "2.119": {"floor": "Second Floor", "x": "85.2%", "y": "45.0%", "type": "Seat"},
    "2.120": {"floor": "Second Floor", "x": "84.3%", "y": "48.2%", "type": "Seat"},
    "2.121": {"floor": "Second Floor", "x": "75.9%", "y": "42.8%", "type": "Seat"},
    "2.122": {"floor": "Second Floor", "x": "75.7%", "y": "46.7%", "type": "Seat"},
    "2.123": {"floor": "Second Floor", "x": "77.6%", "y": "42.8%", "type": "Seat"},
    "2.124": {"floor": "Second Floor", "x": "77.7%", "y": "46.4%", "type": "Seat"},

    "2.125": {"floor": "Second Floor", "x": "69.0%", "y": "35.6%", "type": "Seat"},
    "2.126": {"floor": "Second Floor", "x": "68.9%", "y": "39.3%", "type": "Seat"},
    "2.127": {"floor": "Second Floor", "x": "70.7%", "y": "39.3%", "type": "Seat"},
    "2.128": {"floor": "Second Floor", "x": "70.7%", "y": "35.5%", "type": "Seat"},
    "2.129": {"floor": "Second Floor", "x": "75.7%", "y": "35.8%", "type": "Seat"},
    "2.130": {"floor": "Second Floor", "x": "76.0%", "y": "39.1%", "type": "Seat"},
    "2.131": {"floor": "Second Floor", "x": "77.8%", "y": "35.4%", "type": "Seat"},
    "2.132": {"floor": "Second Floor", "x": "77.8%", "y": "39.1%", "type": "Seat"},

    "2.133": {"floor": "Second Floor", "x": "84.8%", "y": "37.2%", "type": "Seat"},
    "2.134": {"floor": "Second Floor", "x": "83.7%", "y": "40.8%", "type": "Seat"},
    "2.135": {"floor": "Second Floor", "x": "86.6%", "y": "37.7%", "type": "Seat"},
    "2.136": {"floor": "Second Floor", "x": "85.7%", "y": "41.1%", "type": "Seat"},
    "2.137": {"floor": "Second Floor", "x": "86.4%", "y": "30.3%", "type": "Seat"},
    "2.138": {"floor": "Second Floor", "x": "85.4%", "y": "33.7%", "type": "Seat"},
    "2.139": {"floor": "Second Floor", "x": "88.2%", "y": "30.9%", "type": "Seat"},
    "2.140": {"floor": "Second Floor", "x": "87.5%", "y": "34.2%", "type": "Seat"},

    "2.141": {"floor": "Second Floor", "x": "87.9%", "y": "23.5%", "type": "Seat"},
    "2.142": {"floor": "Second Floor", "x": "87.1%", "y": "26.6%", "type": "Seat"},
    "2.143": {"floor": "Second Floor", "x": "89.6%", "y": "24.0%", "type": "Seat"},
    "2.144": {"floor": "Second Floor", "x": "89.0%", "y": "27.2%", "type": "Seat"},
    "2.145": {"floor": "Second Floor", "x": "75.9%", "y": "20.7%", "type": "Seat"},
    "2.146": {"floor": "Second Floor", "x": "75.9%", "y": "24.6%", "type": "Seat"},
    "2.147": {"floor": "Second Floor", "x": "78.0%", "y": "20.7%", "type": "Seat"},
    "2.148": {"floor": "Second Floor", "x": "78.0%", "y": "24.8%", "type": "Seat"},

    "2.149": {"floor": "Second Floor", "x": "69.2%", "y": "28.0%", "type": "Seat"},
    "2.150": {"floor": "Second Floor", "x": "68.9%", "y": "32.0%", "type": "Seat"},
    "2.151": {"floor": "Second Floor", "x": "70.9%", "y": "27.9%", "type": "Seat"},
    "2.152": {"floor": "Second Floor", "x": "71.0%", "y": "31.9%", "type": "Seat"},

    "2.153": {"floor": "Second Floor", "x": "21.9%", "y": "34.4%", "type": "Seat"},
    "2.154": {"floor": "Second Floor", "x": "21.0%", "y": "38.3%", "type": "Seat"},
    "2.155": {"floor": "Second Floor", "x": "19.6%", "y": "33.9%", "type": "Seat"},
    "2.156": {"floor": "Second Floor", "x": "18.9%", "y": "37.4%", "type": "Seat"},

    "2.157": {"floor": "Second Floor", "x": "16.0%", "y": "33.5%", "type": "Seat"},
    "2.158": {"floor": "Second Floor", "x": "15.1%", "y": "36.7%", "type": "Seat"},
    "2.159": {"floor": "Second Floor", "x": "14.0%", "y": "32.9%", "type": "Seat"},
    "2.160": {"floor": "Second Floor", "x": "13.3%", "y": "36.2%", "type": "Seat"},
    "2.161": {"floor": "Second Floor", "x": "12.2%", "y": "32.3%", "type": "Seat"},
    "2.162": {"floor": "Second Floor", "x": "11.3%", "y": "35.8%", "type": "Seat"},
    "2.163": {"floor": "Second Floor", "x": "10.4%", "y": "32.0%", "type": "Seat"},
    "2.164": {"floor": "Second Floor", "x": "9.6%", "y": "35.5%", "type": "Seat"},

    "2.165": {"floor": "Second Floor", "x": "21.3%", "y": "26.8%", "type": "Seat"},
    "2.166": {"floor": "Second Floor", "x": "20.7%", "y": "30.5%", "type": "Seat"},
    "2.167": {"floor": "Second Floor", "x": "23.1%", "y": "27.3%", "type": "Seat"},
    "2.168": {"floor": "Second Floor", "x": "22.4%", "y": "30.9%", "type": "Seat"},

    "2.169": {"floor": "Second Floor", "x": "17.3%", "y": "26.1%", "type": "Seat"},
    "2.170": {"floor": "Second Floor", "x": "16.8%", "y": "29.5%", "type": "Seat"},
    "2.171": {"floor": "Second Floor", "x": "15.7%", "y": "25.7%", "type": "Seat"},
    "2.172": {"floor": "Second Floor", "x": "15.1%", "y": "29.1%", "type": "Seat"},

    "2.173": {"floor": "Second Floor", "x": "11.8%", "y": "25.1%", "type": "Seat"},
    "2.174": {"floor": "Second Floor", "x": "11.2%", "y": "28.3%", "type": "Seat"},
    "2.175": {"floor": "Second Floor", "x": "13.6%", "y": "25.6%", "type": "Seat"},
    "2.176": {"floor": "Second Floor", "x": "13.0%", "y": "28.7%", "type": "Seat"},
    "2.177": {"floor": "Second Floor", "x": "24.7%", "y": "20.3%", "type": "Seat"},
    "2.178": {"floor": "Second Floor", "x": "23.9%", "y": "23.7%", "type": "Seat"},
    "2.179": {"floor": "Second Floor", "x": "22.7%", "y": "20.0%", "type": "Seat"},
    "2.180": {"floor": "Second Floor", "x": "22.0%", "y": "23.3%", "type": "Seat"},

    "2.181": {"floor": "Second Floor", "x": "18.9%", "y": "19.1%", "type": "Seat"},
    "2.182": {"floor": "Second Floor", "x": "18.4%", "y": "22.6%", "type": "Seat"},
    "2.183": {"floor": "Second Floor", "x": "17.2%", "y": "18.9%", "type": "Seat"},
    "2.184": {"floor": "Second Floor", "x": "16.5%", "y": "22.1%", "type": "Seat"},
    "2.185": {"floor": "Second Floor", "x": "15.1%", "y": "18.4%", "type": "Seat"},
    "2.186": {"floor": "Second Floor", "x": "14.3%", "y": "21.7%", "type": "Seat"},
    "2.187": {"floor": "Second Floor", "x": "13.6%", "y": "18.0%", "type": "Seat"},
    "2.188": {"floor": "Second Floor", "x": "12.6%", "y": "21.3%", "type": "Seat"},

    "2.189": {"floor": "Second Floor", "x": "15.1%", "y": "10.8%", "type": "Seat"},
    "2.190": {"floor": "Second Floor", "x": "14.2%", "y": "14.3%", "type": "Seat"},
    "2.191": {"floor": "Second Floor", "x": "16.7%", "y": "11.2%", "type": "Seat"},
    "2.192": {"floor": "Second Floor", "x": "15.7%", "y": "14.6%", "type": "Seat"},
    "2.193": {"floor": "Second Floor", "x": "18.6%", "y": "11.7%", "type": "Seat"},
    "2.194": {"floor": "Second Floor", "x": "17.8%", "y": "15.2%", "type": "Seat"},
    "2.195": {"floor": "Second Floor", "x": "20.2%", "y": "12.3%", "type": "Seat"},
    "2.196": {"floor": "Second Floor", "x": "19.6%", "y": "15.6%", "type": "Seat"},
    "2.197": {"floor": "Second Floor", "x": "24.4%", "y": "12.9%", "type": "Seat"},
    "2.198": {"floor": "Second Floor", "x": "23.6%", "y": "16.4%", "type": "Seat"},
    "2.199": {"floor": "Second Floor", "x": "26.1%", "y": "13.4%", "type": "Seat"},
    "2.200": {"floor": "Second Floor", "x": "25.3%", "y": "16.8%", "type": "Seat"},
}
