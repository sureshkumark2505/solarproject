import os
import joblib

# Build absolute path
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "expected_power_model.pkl")

# Load ML model once
model = joblib.load(MODEL_PATH)

def predict_expected_power(sensor_data):
    """
    sensor_data = {
        "irradiation": float,
        "ambient_temp": float,
        "module_temp": float
    }
    """
    features = [[
        sensor_data["irradiation"],
        sensor_data["ambient_temp"],
        sensor_data["module_temp"],
        sensor_data["wind_speed"]
    ]]

    return round(float(model.predict(features)[0]), 2)
