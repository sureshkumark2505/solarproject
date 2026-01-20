import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 12.9,
        "longitude": 79.1,
        "hourly": "precipitation",
        "forecast_days": 1
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    rain_sum = sum(data["hourly"]["precipitation"])
    return rain_sum > 1, round(rain_sum, 2)
