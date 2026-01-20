import random

def get_sensor_data():
    """
    Simulated Raspberry Pi sensor readings
    Replace with GPIO / I2C / Modbus in real hardware
    """
    return {
        "irradiation": round(random.uniform(400, 1000), 2),
        "ambient_temp": round(random.uniform(25, 40), 2),
        "module_temp": round(random.uniform(30, 55), 2),
        "wind_speed": round(random.uniform(0.5, 6.0), 2)
    }
