import streamlit as st
import requests
import pandas as pd
import datetime
import time
import os
import sys

# Add the whatsapp module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'whatsapp'))
from whatsapp import send_whatsapp_message

API_URL = "http://127.0.0.1:5000/api/summary"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

LAT = 12.9184
LON = 79.1325
REFRESH_SECONDS = 10

HISTORY_FILE = "history.csv"

st.set_page_config(
    page_title="Solar Edge AI Dashboard",
    page_icon="☀️",
    layout="centered"
)

# ------------------------
# STYLE
# ------------------------
st.markdown("""
<style>
.big-number {
    font-size: 36px;
    font-weight: bold;
    color: #ff9800;
}
.card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f9f9f9;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}
.status-good { color: #2e7d32; font-weight: bold; }
.status-warn { color: #f9a825; font-weight: bold; }
.status-bad { color: #c62828; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ------------------------
# DATA FUNCTIONS
# ------------------------
def fetch_solar_data():
    try:
        res = requests.get(API_URL, timeout=5)
        return res.json()
    except:
        return None

def fetch_weather():
    try:
        params = {
            "latitude": LAT,
            "longitude": LON,
            "hourly": "precipitation,cloudcover,wind_speed_10m,relative_humidity_2m,uv_index",
            "forecast_days": 1,
            "timezone": "auto"
        }
        res = requests.get(WEATHER_URL, params=params, timeout=5)
        return res.json()
    except:
        return None

def calculate_weather_summary(weather_json):
    rain = weather_json["hourly"]["precipitation"]
    clouds = weather_json["hourly"]["cloudcover"]

    rain_sum = sum(rain)
    cloud_avg = sum(clouds) / len(clouds)

    return {
        "rain_expected": rain_sum > 1,
        "rain_volume_mm": round(rain_sum, 2),
        "cloud_cover_percent": round(cloud_avg, 1),
        "wind_speed_kmh": weather_json["hourly"]["wind_speed_10m"][0],
        "humidity_percent": weather_json["hourly"]["relative_humidity_2m"][0],
        "uv_index": weather_json["hourly"]["uv_index"][0]
    }

def system_decision(dust_detected, vision_label, avg_loss_percent, rain_expected):
    """
    Decision engine fusing edge data and weather.
    """
    if vision_label == "ElectricalDamage":
        return "🚨 CRITICAL FAULT", "status-bad", "Electrical damage detected. Immediate inspection required."
    elif vision_label == "BirdDroppings":
        return "🧹 CLEANING REQUIRED", "status-bad", "Bird droppings detected on panels."
    elif dust_detected and rain_expected:
        return "🕒 CLEANING POSTPONED", "status-warn", "Dust detected but rain expected for natural cleaning."
    elif dust_detected and not rain_expected:
        return "🚨 ACTION REQUIRED", "status-bad", "Dust detected. Manual cleaning recommended."
    elif avg_loss_percent > 20:
        return "⚠️ HIGH LOSS DETECTED", "status-warn", f"Power loss at {avg_loss_percent}%. Check system."
    else:
        return "✅ SYSTEM HEALTHY", "status-good", "All systems normal."

# ------------------------
# HISTORY TRACKING
# ------------------------
def load_history():
    """Load history from CSV file. Return empty DataFrame if file doesn't exist."""
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame()

def save_history(row):
    df = pd.DataFrame([row])
    if not os.path.exists(HISTORY_FILE):
        df.to_csv(HISTORY_FILE, index=False)
    else:
        df.to_csv(HISTORY_FILE, mode="a", header=False, index=False)

def send_cleaning_request(method):
    """
    Send cleaning request to API.
    """
    clean_url = "http://127.0.0.1:5000/api/clean"
    data = {
        "method": method,
        "message": f"Panel cleaning required. Method: {method}"
    }
    try:
        requests.post(clean_url, json=data, timeout=5)
    except:
        pass  # Ignore errors for demo

# ------------------------
# MAIN
# ------------------------
st.markdown("## ☀️ Solar Edge AI Dashboard")
st.caption("Raspberry Pi → Edge AI → API → Mobile Dashboard")

solar = fetch_solar_data()
weather_raw = fetch_weather()

if solar is None or "error" in solar or weather_raw is None:
    st.error("Unable to connect to Edge API or Weather Service")
    st.stop()

weather = calculate_weather_summary(weather_raw)

# Save history
# Safely choose a time key from the solar summary. If missing, use current time.
if "date" in solar:
    time_key = "date"
elif "timestamp" in solar:
    time_key = "timestamp"
else:
    time_key = None

if time_key and time_key in solar:
    time_value = solar[time_key]
else:
    # Fall back to current UTC time ISO string
    time_value = datetime.datetime.utcnow().isoformat()

history_row = {
    "time": time_value,
    "expected_power": solar.get("expected_power"),
    "avg_loss_percent": solar.get("avg_loss_percent"),
    "health_score": solar.get("health_score"),
    "vision_label": solar.get("vision_label"),
    "dust_detected": solar.get("dust_detected")
}
save_history(history_row)

history_df = load_history()

# ------------------------
# STATUS CARD
# ------------------------
status, status_class, status_reason = system_decision(
    solar["dust_detected"],
    solar["vision_label"],
    solar["avg_loss_percent"],
    weather["rain_expected"]
)

st.markdown(f"""
<div class="card">
    <div class="{status_class}">{status}</div>
    <div>{status_reason}</div>
</div>
""", unsafe_allow_html=True)

# ------------------------
# CLEANING OPTIONS
# ------------------------
if "ACTION REQUIRED" in status or "CLEANING REQUIRED" in status:
    st.markdown("### 🧹 Select Cleaning Method")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Robot Cleaning"):
            send_cleaning_request("robot")
            st.success("Cleaning request sent to Robot!")
    
    with col2:
        if st.button("💧 Pressurized Water"):
            send_cleaning_request("pressurized_water")
            st.success("Cleaning request sent to Pressurized Water system!")
    
    with col3:
        if st.button("👷 Cleaning Agency"):
            send_cleaning_request("cleaning_agency")
            # Send WhatsApp message
            whatsapp_message = "🚨 Solar Panel Cleaning Required: Dust detected. Please send cleaning agency immediately."
            if send_whatsapp_message(whatsapp_message):
                st.success("Cleaning request sent to Cleaning Agency and WhatsApp!")
            else:
                st.success("Cleaning request sent to Cleaning Agency! (WhatsApp demo mode)")

# ------------------------
# PANEL IMAGE
# ------------------------
if "panel_image" in solar:
    import base64
    image_data = base64.b64decode(solar["panel_image"])
    st.image(image_data, caption="Panel Image", width=222)

# ------------------------
# METRICS
# ------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Expected Power")
    st.markdown(f"<div class='big-number'>{solar['expected_power']} W</div>", unsafe_allow_html=True)

    st.markdown("### 🏥 Health Score")
    st.markdown(f"<div class='big-number'>{solar['health_score']}%</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📉 Avg Loss %")
    st.markdown(f"<div class='big-number'>{solar['avg_loss_percent']}%</div>", unsafe_allow_html=True)

    st.markdown("### 👁 Vision Label")
    st.markdown(f"<div class='big-number'>{solar['vision_label']}</div>", unsafe_allow_html=True)

# ------------------------
# GRAPHS
# ------------------------
st.markdown("## 📊 Performance Graph (8 AM - 6 PM)")

if len(history_df) > 2:
    history_df["time"] = pd.to_datetime(history_df["time"])
    # Filter to daytime hours 8 AM to 6 PM
    daytime_df = history_df[(history_df["time"].dt.hour >= 8) & (history_df["time"].dt.hour <= 18)]

    if len(daytime_df) > 0:
        st.line_chart(
            daytime_df.set_index("time")[["expected_power"]],
            height=250
        )
    else:
        st.info("No daytime data available for graph.")
else:
    st.info("Collecting data for performance visualization...")

# ------------------------
# WEATHER
# ------------------------
st.markdown("## 🌦 Weather Conditions")

wcol1, wcol2 = st.columns(2)

with wcol1:
    st.write("🌧 Rain Expected:", "Yes" if weather["rain_expected"] else "No")
    st.write("☁ Cloud Cover:", f"{weather['cloud_cover_percent']} %")
    st.write("💧 Humidity:", f"{weather['humidity_percent']} %")

with wcol2:
    st.write("🌬 Wind Speed:", f"{weather['wind_speed_kmh']} km/h")
    st.write("🌞 UV Index:", weather["uv_index"])
    st.write("🌧 Rain Volume:", f"{weather['rain_volume_mm']} mm")

st.caption("Powered by Raspberry Pi Edge AI • Open-Meteo • Streamlit")

# Auto refresh
time.sleep(REFRESH_SECONDS)
st.rerun()
