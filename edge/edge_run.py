import json
import random
from datetime import datetime

# Simulate edge AI outputs
def generate_summary():
    avg_loss = round(random.uniform(3, 15), 2)
    dust_detected = avg_loss > 8

    forecasted_energy = round(random.uniform(3500, 5200), 2)

    health_score = 100 - avg_loss
    if dust_detected:
        health_score -= 15

    health_score = max(0, min(100, round(health_score, 1)))

    summary = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "dust_detected": dust_detected,
        "avg_loss_percent": avg_loss,
        "forecasted_energy_kWh": forecasted_energy,
        "health_score": health_score
    }

    return summary

# Write summary to file
summary = generate_summary()

with open("summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("EDGE SUMMARY GENERATED:")
print(json.dumps(summary, indent=2))
