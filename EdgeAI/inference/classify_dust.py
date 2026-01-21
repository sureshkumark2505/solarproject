import os
from ultralytics import YOLO

# Absolute path to model
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "best1.pt")

# Load YOLO model once
model = YOLO(MODEL_PATH)

CLASS_NAMES = [
    "Clean",
    "Dust",
    "BirdDroppings",
    "ElectricalDamage"
]

def classify_panel(image_path):
    try:
        results = model(image_path, verbose=False)
        print(f"Vision results: {len(results[0].boxes)} boxes found")

        if len(results[0].boxes) == 0:
            print("No detections, returning Clean")
            return "Clean"

        best_box = max(results[0].boxes, key=lambda b: float(b.conf))
        class_id = int(best_box.cls)
        confidence = float(best_box.conf)
        print(f"Best detection: class {class_id} ({CLASS_NAMES[class_id]}) with conf {confidence}")

        return CLASS_NAMES[class_id]

    except Exception as e:
        print("Vision Error:", e)
        return "Clean"  # Changed to "Clean" instead of "Unknown"
