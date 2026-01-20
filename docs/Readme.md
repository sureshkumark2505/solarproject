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

## 📁 Folder Structure

```
solar-app/
│
├── edge/                       # Simulated Raspberry Pi / Edge AI
│   ├── edge_run.py            # ML model + dust + loss + forecast logic
│   ├── model.pkl             # Trained expected power model
│   ├── sensors.py           # Sensor simulation (optional)
│   ├── config.py            # Thresholds & system constants
│   └── requirements.txt     # Python dependencies
│
├── api/                      # Backend REST API
│   ├── server.js            # Node Express server
│   ├── package.json
│   └── routes/
│       └── summary.js      # /api/summary endpoint
│
├── dashboard/               # Mobile Dashboard (Streamlit)
│   ├── dashboard.py        # UI + Weather + Decision Engine
│   └── requirements.txt
│
├── data/                   # Datasets & logs
│   ├── raw/               # Original CSV datasets
│   ├── processed/        # Cleaned datasets
│   └── logs/             # System logs
│
├── docs/                  # Presentation & Documentation
│   ├── architecture.png
│   ├── ppt_storyline.md
│   └── demo_script.txt
│
├── scripts/
│   └── run_all.bat       # One-click system launcher
│
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

| Layer     | Technology                     |
| --------- | ------------------------------ |
| Edge AI   | Python, Scikit-learn, Pandas   |
| API       | Node.js, Express, CORS         |
| Dashboard | Streamlit                      |
| Weather   | Open-Meteo API                 |
| ML Model  | Random Forest Regressor        |
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

* ⚡ Live Power Display
* 🏥 Plant Health Score
* 🧹 Cleaning Recommendation
* 🌧 Weather Conditions
* 📊 Daily Energy Chart
* 🔔 Status Alerts

Works on:

* Mobile phones
* Tablets
* Laptops

---

## ▶️ How to Run the Full System

### 1️⃣ Install Dependencies

#### Edge

```bash
cd edge
pip install -r requirements.txt
```

#### API

```bash
cd api
npm install
```

#### Dashboard

```bash
cd dashboard
pip install -r requirements.txt
```

---

### 2️⃣ Start System (Manual)

#### Terminal 1 – Edge AI

```bash
cd edge
python edge_run.py
```

#### Terminal 2 – API Server

```bash
cd api
node server.js
```

#### Terminal 3 – Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

---

### 3️⃣ Open Dashboard

On Laptop:

```
http://localhost:8501
```

On Phone (same WiFi):

```
http://<your-ip>:8501
```

---

## ⚡ One-Click Run (Windows)

Use:

```
scripts/run_all.bat
```

This launches:

* Edge AI
* API Server
* Mobile Dashboard

---

## 🧪 Sample API Output

```json
{
  "forecasted_energy_kWh": 4740.15,
  "avg_loss_percent": 13.53,
  "dust_detected": true,
  "health_score": 86.47
}
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

## 📜 License

This project is for academic, hackathon, and research use. Free to extend and modify.

---

## ⭐ Final Note

This project demonstrates:

> **Edge AI + Cloud Architecture + Mobile UX + Sustainable Technology**

A complete, real-world inspired smart energy system — not just a machine learning model.

---

If you’re a judge, recruiter, or collaborator — feel free to reach out! ☀️🚀


