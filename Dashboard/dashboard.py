import streamlit as st
import requests
import pandas as pd
import datetime
import time
import os

API_URL = "http://127.0.0.1:5000/api/summary"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

LAT = 12.9184
LON = 79.1325
REFRESH_SECONDS = 10

HISTORY_FILE = "history.csv"

st.set_page_config(
    page_title="Solar Edge AI Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------
# STYLE
# ------------------------
st.markdown("""
<style>
.big-number {
    font-size: 24px;
    font-weight: bold;
    color: #ff9800;
}
.card {
    padding: 10px;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 8px;
}
.status-good { color: #2e7d32; font-weight: bold; font-size: 14px; }
.status-warn { color: #f9a825; font-weight: bold; font-size: 14px; }
.status-bad { color: #c62828; font-weight: bold; font-size: 14px; }
h2 { font-size: 18px; margin: 10px 0 5px 0; }
h3 { font-size: 14px; margin: 8px 0 3px 0; }
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
            "daily": "uv_index_max",
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
    uv_hourly = weather_json["hourly"]["uv_index"]
    
    # Get daily max UV index
    uv_max = weather_json["daily"]["uv_index_max"][0] if "daily" in weather_json and "uv_index_max" in weather_json["daily"] else max(uv_hourly)

    rain_sum = sum(rain)
    cloud_avg = sum(clouds) / len(clouds)
    uv_current = uv_hourly[0]

    return {
        "rain_expected": rain_sum > 1,
        "rain_volume_mm": round(rain_sum, 2),
        "cloud_cover_percent": round(cloud_avg, 1),
        "wind_speed_kmh": weather_json["hourly"]["wind_speed_10m"][0],
        "humidity_percent": weather_json["hourly"]["relative_humidity_2m"][0],
        "uv_index": round(uv_current, 2),
        "uv_index_max": round(uv_max, 2)
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
    """Save history row only if it's not a duplicate."""
    df = pd.DataFrame([row])
    
    if not os.path.exists(HISTORY_FILE):
        df.to_csv(HISTORY_FILE, index=False)
        return
    
    # Load existing data
    existing_df = pd.read_csv(HISTORY_FILE)
    
    # Check for duplicate (same time, expected_power, and problem)
    if len(existing_df) > 0:
        time_match = existing_df['time'] == row['time']
        power_match = existing_df['expected_power'] == row['expected_power']
        
        # Check problem column if it exists
        if 'problem' in existing_df.columns and 'problem' in row:
            problem_match = existing_df['problem'] == row['problem']
            duplicate = existing_df[time_match & power_match & problem_match]
        else:
            duplicate = existing_df[time_match & power_match]
            
        if len(duplicate) > 0:
            # Duplicate found, don't save
            return
    
    # No duplicate, append
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

# Add refresh button
col_refresh = st.columns([5, 1])
with col_refresh[1]:
    if st.button("🔄 Refresh", key="refresh_btn"):
        st.rerun()

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
    # Fall back to standard datetime format
    time_value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Determine problem based on system status
problem = "None"
if solar.get("dust_detected"):
    problem = "Dust Detected"
elif solar.get("vision_label") == "BirdDroppings":
    problem = "Bird Droppings"
elif solar.get("vision_label") == "ElectricalDamage":
    problem = "Electrical Damage"
elif solar.get("avg_loss_percent", 0) > 20:
    problem = f"High Loss ({solar.get('avg_loss_percent')}%)"

history_row = {
    "time": time_value,
    "expected_power": solar.get("expected_power"),
    "actual_power": solar.get("expected_power", 0) * (1 - solar.get("avg_loss_percent", 0) / 100),
    "avg_loss_percent": solar.get("avg_loss_percent"),
    "health_score": solar.get("health_score"),
    "vision_label": solar.get("vision_label"),
    "problem": problem
}
save_history(history_row)

history_df = load_history()

# ------------------------
# STATUS CARD
# ------------------------
status, status_class, status_reason = system_decision(
    solar.get("dust_detected", False),
    solar.get("vision_label", "Clean"),
    solar.get("avg_loss_percent", 0),
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
            st.success("Cleaning request sent to Cleaning Agency!")

# ------------------------
# PANEL IMAGE
# ------------------------
if "panel_image" in solar:
    import base64
    image_data = base64.b64decode(solar["panel_image"])
    st.image(image_data, caption="Panel Image", width=150)

# ------------------------
# METRICS
# ------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Expected Power")
    st.markdown(f"<div class='big-number'>{solar.get('expected_power', 0):.0f} W</div>", unsafe_allow_html=True)

    st.markdown("### 🏥 Health Score")
    st.markdown(f"<div class='big-number'>{solar.get('health_score', 0):.0f}%</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📉 Loss %")
    st.markdown(f"<div class='big-number'>{solar.get('avg_loss_percent', 0):.1f}%</div>", unsafe_allow_html=True)

    st.markdown("### 👁 Vision")
    st.markdown(f"<div class='big-number'>{solar.get('vision_label', 'N/A')}</div>", unsafe_allow_html=True)

# ------------------------
# GRAPHS
# ------------------------
st.markdown("## 📊 Performance Graph (8 AM - 6 PM)")

if len(history_df) > 2:
    history_df["time"] = pd.to_datetime(history_df["time"], format="mixed", utc=False)
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
# FORECAST GRAPH (Dummy 7-hour forecast)
# ------------------------
st.markdown("## 📈 Today's Energy Forecast")

hours = ["6 AM", "8 AM", "10 AM", "12 PM", "2 PM", "4 PM", "6 PM"]
forecasted_energy = solar.get("forecasted_energy_kWh", 100)
forecast = [
    forecasted_energy * 0.05,
    forecasted_energy * 0.12,
    forecasted_energy * 0.22,
    forecasted_energy * 0.28,
    forecasted_energy * 0.20,
    forecasted_energy * 0.10,
    forecasted_energy * 0.03,
]

forecast_df = pd.DataFrame({
    "Time": hours,
    "Energy (kWh)": forecast
})

st.bar_chart(forecast_df.set_index("Time"), height=250)

# ------------------------
# LAST 5 DAYS SUMMARY TABLE
# ------------------------
st.markdown("## 📅 Last 5 Days Summary")

if len(history_df) > 0:
    # Convert time to datetime - handle mixed formats
    history_df["time"] = pd.to_datetime(history_df["time"], format="mixed", utc=False)
    
    # Sort by time descending and take last 5 days
    history_df_sorted = history_df.sort_values("time", ascending=False).head(5)
    
    # Reorder columns for display
    display_df = history_df_sorted[["time", "expected_power", "actual_power", "avg_loss_percent", "problem"]].copy()
    display_df.columns = ["Date", "Expected Power (W)", "Actual Power (W)", "Loss %", "Problem"]
    
    # Round power values
    display_df["Expected Power (W)"] = display_df["Expected Power (W)"].round(1)
    display_df["Actual Power (W)"] = display_df["Actual Power (W)"].round(1)
    display_df = display_df.reset_index(drop=True)
    
    # Display as table
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No historical data available yet.")

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
    st.write("🌞 Current UV:", weather.get("uv_index", 0))
    st.write("☀️ Max UV Today:", weather.get("uv_index_max", 0))

st.caption("Powered by Raspberry Pi Edge AI • Open-Meteo • Streamlit")

# Remove auto-refresh - user controls it with button
# Uncomment below if you want auto-refresh
# time.sleep(REFRESH_SECONDS)
# st.rerun()
