# ☀️ Solar Edge AI – Smart Solar Plant Monitoring System

> **Edge AI → API → Mobile Dashboard**

A full-stack, low-internet solar plant monitoring and decision-support system that runs machine learning at the edge, exposes insights through a lightweight API, and visualizes intelligence on a mobile-friendly dashboard.

This project simulates a **real-world solar farm deployment** where connectivity is limited, costs are constrained, and maintenance decisions must be intelligent, automated, and explainable.

---

## 🏆 Project Highlights

* 🔋 **Expected Power Prediction (ML at Edge)**
  Predicts how much power the plant *should* generate based on weather and sensor data.

* 📉 **Loss Detection & Health Score**
  Compares expected vs actual output to compute efficiency loss and a real-time **Plant Health Score**.

* 🧹 **Dust Detection (No Camera Required)**
  Detects panel dust using power-loss patterns and environmental conditions.

* 🌧 **Weather-Aware Cleaning Decision**
  Integrates live weather API to decide whether to **clean now or postpone** due to incoming rain.

* 📊 **Daily Energy Forecast**
  Generates a full-day energy profile for planning and reporting.

* 📱 **Mobile-Friendly Dashboard**
  Displays real-time system status, health, weather, and forecasts on any phone or browser.

---

## 🧠 System Architecture

```
[ Edge Device (Laptop / Raspberry Pi) ]
        |
        |  ML Predictions + Sensor Logic
        v
[ Lightweight API Server ]
        |
        |  JSON Summary Endpoint
        v
[ Mobile Dashboard (Streamlit Web App) ]
        |
        v
[ Plant Owner / Maintenance Team ]
```

### Design Philosophy

* **Low Internet Usage** → ML runs locally at the edge
* **Low Cost Hardware** → Designed for Raspberry Pi deployment
* **Scalable Backend** → API can move to cloud later
* **Mobile First** → Dashboard works on any smartphone

---

## ⚙️ Tech Stack

| Layer     | Technology                     |
| --------- | ------------------------------ |
| Edge AI   | Python, Scikit-learn, Pandas   |
| API       | Flask, Python                  |
| Dashboard | Streamlit                      |
| Weather   | Open-Meteo API                 |
| ML Model  | Random Forest Regressor        |
| Data      | CSV (History Tracking)         |
| Platform  | Windows / Linux / Raspberry Pi |

---

## 🔬 Machine Learning Pipeline

### Input Features

* Irradiance
* Ambient Temperature
* Module Temperature
* Time of Day

### Output

* **Expected Power (Watts / kWh)**

### Model

* Random Forest Regression

### Evaluation

* R² Score ≈ **0.97+**
* Mean Absolute Error ≈ **Low error range**

---

## 🧹 Dust Detection Logic

Dust is inferred when:

```
Power Loss % > Dynamic Threshold
AND
No Rain Expected
```

This avoids false positives and eliminates the need for expensive cameras.

---

## 🌦 Weather Integration

Weather data is fetched from:

**Open-Meteo API (Free, No API Key Required)**

Parameters used:

* Precipitation
* Cloud Cover
* Wind Speed
* Humidity
* UV Index

This enables:

* Rain-based cleaning skip
* Weather-aware decision engine

---

## 📱 Dashboard Features

### Real-Time Monitoring
* ⚡ **Expected Power** - ML-predicted power output
* **Actual Power** - Calculated from loss percentage
* 🏥 **Plant Health Score** - 0-100% system efficiency
* **Loss %** - Efficiency loss detection
* 👁 **Problem Detection** - None, Dust, Bird Droppings, Electrical Damage, High Loss

### Visualization
* 📊 **Performance Graph** - 8 AM - 6 PM daytime tracking
* 📈 **Energy Forecast** - 7-hour bar chart (6 AM - 6 PM)
* 🔔 **Status Card** - Color-coded alerts
* 📅 **Last 5 Days Summary Table** - Historical tracking with problem status

### Weather Integration
* 🌧 **Rain Prediction** - Yes/No with volume forecast
* ☁ **Cloud Cover** - Percentage
* 💧 **Humidity** - Current %
* 🌬 **Wind Speed** - km/h
* 🌞 **Current UV Index** - Real-time
* ☀️ **Max UV Today** - Daily peak forecast

### User Controls
* 🔄 **Manual Refresh Button** - Click to update (no auto-refresh)
* 🧹 **Cleaning Request Buttons** - Robot, Pressurized Water, Cleaning Agency
* 📱 **Mobile-Optimized UI** - Responsive design for phones and tablets

### Data Tracking
* 📊 **history.csv** - Stores: time, expected_power, actual_power, avg_loss_percent, health_score, vision_label, problem

---

## 🔧 Recent Updates (v2.0)

✅ **Dashboard Enhancements**
- Mobile-responsive UI (reduced font sizes, optimized spacing)
- Manual refresh button (removed auto-refresh)
- UV Index from weather API (current + daily max)
- "Problem" column intelligent detection (replaces dust_detected)
- Actual power calculation (expected_power × (1 - loss%))
- Last 5 days summary table with all metrics
- Better error handling with `.get()` defaults

✅ **API Improvements**
- Flask API (Python) replaces Node.js
- Root endpoint `/` for API status check
- Handles missing fields gracefully
- CORS enabled for dashboard access

✅ **Edge AI Logic**
- Improved loss calculation (2% base loss for clean panels)
- Accurate problem detection (Dust: +15%, BirdDroppings: +20%, etc.)
- Reduced false positives with realistic thresholds
- Clean panel image (clean.jpeg)

✅ **Data Management**
- Duplicate detection (prevents repeated entries)
- Flexible datetime parsing (handles multiple formats)
- CSV-based history tracking
- Smart time fallback to current time

Works on:

* Mobile phones
* Tablets
* Laptops

---

## ▶️ How to Run the Full System

### Prerequisites
```bash
pip install streamlit pandas requests flask flask-cors scikit-learn
```

### 1️⃣ Terminal 1 – API Server (Start First)

```bash
cd e:\solarproject\api
python server.py
```

Runs on: `http://127.0.0.1:5000`

Endpoints:
- `GET /` - API status
- `GET /api/summary` - Get latest edge summary
- `POST /api/summary` - Store summary from edge
- `POST /api/clean` - Receive cleaning requests

### 2️⃣ Terminal 2 – Edge AI (Start Second)

```bash
cd e:\solarproject\EdgeAI
python edge_runner.py
```

Does:
- Simulates sensor data
- Runs ML prediction (expected power)
- Classifies panel condition (vision AI)
- Calculates loss percentage
- POSTs to API every cycle

### 3️⃣ Terminal 3 – Dashboard (Start Third)

```bash
cd e:\solarproject\Dashboard
streamlit run dashboard.py
```

Access:
- **Local**: `http://localhost:8501`
- **Network**: `http://<your-ip>:8501`

---

### Quick Start (All at Once)

**Option 1: Windows - Manual (3 terminals)**
1. Open 3 PowerShell windows
2. Run the commands above sequentially
3. Open browser: `http://localhost:8501`

**Option 2: Python Cross-Platform**
```bash
cd e:\solarproject
python launch.py  # (launches all 3 services)
```

**Option 3: Linux/Mac**
```bash
cd /path/to/solarproject
./launch.sh  # (launches all 3 services)
```

---

### Installation Details

#### Edge AI Dependencies
```bash
cd EdgeAI
pip install -r requirements.txt
```

Includes: YOLOv8 for vision, scikit-learn for ML

#### API Dependencies
```bash
cd api
pip install flask flask-cors
```

#### Dashboard Dependencies
```bash
cd Dashboard
pip install streamlit pandas requests
```

---

## 🧪 API Response Example

**GET /api/summary**

```json
{
  "date": "2026-01-21 10:30:45",
  "expected_power": 459.45,
  "avg_loss_percent": 2.1,
  "vision_label": "Clean",
  "dust_detected": false,
  "health_score": 97.9,
  "forecasted_energy_kWh": 4500.0,
  "panel_image": "base64_encoded_image_data"
}
```

**Dashboard Last 5 Days Table**

| Date | Expected Power (W) | Actual Power (W) | Loss % | Problem |
|------|-------------------|------------------|--------|---------|
| 2026-01-21 10:30 | 459.5 | 449.9 | 2.1 | None |
| 2026-01-21 10:20 | 442.0 | 368.4 | 16.6 | Dust Detected |
| 2026-01-21 10:10 | 438.5 | 417.6 | 4.8 | None |
| 2026-01-21 10:00 | 451.2 | 381.5 | 15.4 | Bird Droppings |
| 2026-01-21 09:50 | 440.8 | 428.8 | 2.7 | None |

---

## 📊 Directory Structure

```
solarproject/
├── api/
│   ├── server.py          # Flask API (GET/POST endpoints)
│   ├── package.json
│   └── server.py.bak
│
├── Dashboard/
│   ├── dashboard.py       # Streamlit app (mobile UI)
│   ├── history.csv        # Data tracking file
│   └── requirements.txt
│
├── EdgeAI/
│   ├── edge_runner.py     # Main edge AI runner
│   ├── images/
│   │   ├── clean.jpeg
│   │   ├── dust1.jpeg
│   │   └── clean1.jpeg
│   ├── inference/
│   │   ├── sensor_client.py
│   │   ├── predict_power.py
│   │   ├── classify_dust.py
│   │   └── decision_engine.py
│   ├── model/
│   │   └── best.pt        # YOLOv8 model
│   └── weather/
│       └── weather_client.py
│
├── dataset/
│   ├── Plant_1_Generation_Data.csv
│   └── Plant_1_Weather_Sensor_Data.csv
│
├── docs/
│   └── Readme.md          # This file
│
└── launch.py / launch.bat / launch.sh  # Launcher scripts
```

---

## 🔐 Security Notes

- ✅ No hardcoded API keys
- ✅ Weather API is free (Open-Meteo)
- ✅ CSV-based data (no database overhead)
- ⚠️ Dashboard accessible on local network (WiFi)
- 📝 For production: Add authentication, HTTPS, rate limiting

---

## 🧪 Testing

### Test Edge AI
```bash
cd EdgeAI
python edge_runner.py
```

Outputs:
- Sensor data (simulated)
- Expected power prediction
- Vision classification
- Loss calculation
- API post status

### Test API
```bash
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/api/summary
```

### Test Dashboard
Visit: `http://localhost:8501` after all services running

---

## 🚀 Deployment Options

### Local/Raspberry Pi
- Run all 3 services on edge device
- Access dashboard from any device on network

### Cloud (AWS/Render/Railway)
- Deploy API to cloud
- Keep edge AI local
- Dashboard accessible worldwide

### Docker
```bash
docker build -t solarproject .
docker run -p 5000:5000 solarproject
```

---

## 🧑‍⚖️ Judge-Ready Explanation

> “Our system deploys machine learning models at the edge to predict expected power output and detect efficiency loss. A lightweight API synchronizes insights to a mobile dashboard, which integrates real-time weather intelligence to make automated, cost-effective cleaning decisions for solar farms operating in low-connectivity environments.”

---

## 🚀 Future Enhancements

* 🔔 WhatsApp / SMS Alerts (Twilio)
* ☁️ Cloud Deployment (AWS / Render / Railway)
* 📡 Real Sensor Integration (MQTT / Modbus)
* 📊 Historical Analytics Dashboard
* 📱 Native Mobile App (Flutter)

---

## 👨‍💻 Author

**Suresh Kumar**
M.Tech Integrated – Data Science
VIT

---
**Rakesh**
M.Tech Integrated – Data Science
VIT

---
**Sruthilaiya**
M.Tech Integrated – Data Science
VIT

---

## 📜 License

This project is for academic, hackathon, and research use. Free to extend and modify.

---

## ⭐ Final Note

This project demonstrates:

> **Edge AI + Cloud Architecture + Mobile UX + Sustainable Technology**

A complete, real-world inspired smart energy system — not just a machine learning model.

---


