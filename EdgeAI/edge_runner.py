import json
import time
import requests
from datetime import datetime
import random  # For simulation
import base64
import os

from inference.sensor_client import get_sensor_data
from inference.predict_power import predict_expected_power
from inference.classify_dust import classify_panel

BASE_DIR = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_DIR, "images", "dust1.jpeg")
print(f"Image path: {IMAGE_PATH}")
API_URL = "http://127.0.0.1:5000/api/summary"

def check_internet():
    """
    Check if internet is available.
    """
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

def simulate_sensors():
    """
    Simulate solar sensor data.
    In production, this would read from actual sensors.
    """
    return {
        "irradiation": round(random.uniform(200, 1000), 2),
        "ambient_temp": round(random.uniform(20, 40), 2),
        "module_temp": round(random.uniform(25, 50), 2),
        "wind_speed": round(random.uniform(0, 10), 2)
    }

def compute_loss_percent(sensor_data, vision_label):
    """
    Compute average loss percentage based on sensor data and vision label.
    Loss should reflect actual panel condition, not random values.
    """
    base_loss = 2.0  # Base system loss (very low for clean panels)
    
    if vision_label == "Dust":
        base_loss += 15.0  # Dust causes 15% additional loss
    elif vision_label == "BirdDroppings":
        base_loss += 20.0  # Bird droppings cause 20% additional loss
    elif vision_label == "ElectricalDamage":
        base_loss += 50.0  # Electrical damage causes 50% additional loss
    elif vision_label == "Clean":
        base_loss = 1.0  # Clean panels have minimal loss
    else:
        base_loss = 2.0  # Default minimal loss
    
    # Add small random variation (±0.5%) for realism
    variation = round(random.uniform(-0.5, 0.5), 2)
    final_loss = max(0.5, base_loss + variation)  # Ensure minimum 0.5% loss
    
    return round(final_loss, 2)

def run_edge():
    """
    Run edge AI once and send summary.
    """
    print("\n🌐 Running edge AI...")

    sensor_data = simulate_sensors()
    print("Sensor data:", sensor_data)

    expected_power = predict_expected_power(sensor_data)
    print("Expected Power:", expected_power, "W")

    vision_label = classify_panel(IMAGE_PATH)
    print("Vision Label:", vision_label)

    avg_loss_percent = compute_loss_percent(sensor_data, vision_label)
    health_score = 100 - avg_loss_percent
    dust_detected = vision_label == "Dust"

    # Encode image
    with open(IMAGE_PATH, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')

    summary = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expected_power": expected_power,
        "avg_loss_percent": avg_loss_percent,
        "vision_label": vision_label,
        "dust_detected": dust_detected,
        "health_score": health_score,
        "panel_image": image_data
    }

    response = requests.post(API_URL, json=summary, timeout=10)
    if response.status_code == 200:
        print("Summary sent successfully")
    else:
        print(f"Failed to send: {response.status_code}")

if __name__ == "__main__":
    run_edge()
