import streamlit as st
import requests
import pandas as pd
import datetime
import time

# -----------------------------
# CONFIG
# -----------------------------
API_URL = "http://127.0.0.1:5000/api/summary"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

LAT = 12.9184
LON = 79.1325

REFRESH_SECONDS = 10

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="Solar Edge AI Dashboard",
    page_icon="☀️",
    layout="centered"
)

st.markdown(
    """
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
    .status-good {
        color: #2e7d32;
        font-weight: bold;
    }
    .status-warn {
        color: #f9a825;
        font-weight: bold;
    }
    .status-bad {
        color: #c62828;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# HELPERS
# -----------------------------
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


def system_decision(dust, rain_expected):
    if dust and rain_expected:
        return "🕒 CLEANING POSTPONED", "status-warn", "Rain expected. Natural cleaning will occur."
    elif dust and not rain_expected:
        return "🚨 ACTION REQUIRED", "status-bad", "Dust detected. Manual cleaning recommended."
    else:
        return "✅ SYSTEM HEALTHY", "status-good", "Panels are clean. No action required."


# -----------------------------
# TITLE
# -----------------------------
st.markdown("## ☀️ Solar Edge AI Dashboard")
st.caption("Edge AI → API → Mobile Dashboard (Low Internet Architecture)")

# Auto refresh
st.empty()
time.sleep(0.1)
# st.rerun()  # Commented out to prevent infinite loop

# -----------------------------
# FETCH DATA
# -----------------------------
solar = fetch_solar_data()
weather_raw = fetch_weather()

if solar is None or weather_raw is None:
    st.error("Unable to connect to Edge API or Weather Service")
    st.stop()

weather = calculate_weather_summary(weather_raw)

# -----------------------------
# ENRICH DATA
# -----------------------------
current_power = round((solar["forecasted_energy_kWh"] / 24) * 1.2, 2)
health_score = round(100 - solar["avg_loss_percent"], 2)

status, status_class, status_reason = system_decision(
    solar["dust_detected"],
    weather["rain_expected"]
)

# -----------------------------
# STATUS CARD
# -----------------------------
st.markdown(
    f"""
    <div class="card">
        <div class="{status_class}">{status}</div>
        <div>{status_reason}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# METRICS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Current Power")
    st.markdown(f"<div class='big-number'>{current_power} kW</div>", unsafe_allow_html=True)

    st.markdown("### 📈 Energy Forecast")
    st.markdown(f"<div class='big-number'>{solar['forecasted_energy_kWh']} kWh</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🏥 Health Score")
    st.markdown(f"<div class='big-number'>{health_score} %</div>", unsafe_allow_html=True)

    st.markdown("### 📉 Avg Loss")
    st.markdown(f"<div class='big-number'>{solar['avg_loss_percent']} %</div>", unsafe_allow_html=True)

# -----------------------------
# SYSTEM INFO
# -----------------------------
st.markdown("## 🔧 System Health")

sys_col1, sys_col2 = st.columns(2)

with sys_col1:
    st.write("🧹 Dust Detected:", "Yes" if solar["dust_detected"] else "No")
    st.write("📆 Date:", datetime.datetime.now().strftime("%Y-%m-%d"))

with sys_col2:
    st.write("🔋 Efficiency:", f"{health_score}%")
    st.write("📡 Data Source:", "Edge AI Node")

# -----------------------------
# WEATHER
# -----------------------------
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

# -----------------------------
# DAILY ENERGY FORECAST CHART
# -----------------------------
st.markdown("## 📊 Daily Energy Forecast")

hours = ["6 AM", "8 AM", "10 AM", "12 PM", "2 PM", "4 PM", "6 PM"]
forecast = [
    solar["forecasted_energy_kWh"] * 0.05,
    solar["forecasted_energy_kWh"] * 0.12,
    solar["forecasted_energy_kWh"] * 0.22,
    solar["forecasted_energy_kWh"] * 0.28,
    solar["forecasted_energy_kWh"] * 0.20,
    solar["forecasted_energy_kWh"] * 0.10,
    solar["forecasted_energy_kWh"] * 0.03,
]

df = pd.DataFrame({
    "Time": hours,
    "Forecasted Energy (kWh)": forecast
})

st.line_chart(df.set_index("Time"))

# -----------------------------
# FOOTER
# -----------------------------
st.caption("Powered by Edge AI • Weather API • Streamlit Mobile UI")
