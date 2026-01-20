LOSS_THRESHOLD = 8.0

def make_decision(expected_power, vision_result):
    """
    Multi-modal Edge Decision Engine
    Inputs:
    - expected_power: float (ML power prediction)
    - vision_result: str (Clean, Dust, BirdDroppings, ElectricalDamage)
    Output:
    - Human-readable action decision
    - dust_flag: bool (whether dust is detected)
    """

    vision_label = vision_result.strip()
    rain_expected = False  # Assume no rain for simplicity
    loss_percent = 0  # Assume no loss for now, or calculate if needed

    dust_flag = vision_label == "Dust"

    # 1️⃣ Critical faults override everything
    if vision_label == "ElectricalDamage":
        return "🚨 CRITICAL: Electrical Fault - Shutdown & Inspect Immediately", dust_flag

    # 2️⃣ Bird droppings cause hotspots & permanent damage
    if vision_label == "BirdDroppings":
        if rain_expected:
            return "🕒 Postpone Cleaning - Rain Expected", dust_flag
        return "🧹 Cleaning Required - Bird Droppings Detected", dust_flag

    if expected_power < 200:
        return "⚠️ Low Power Output - Check Inverter or Shading", dust_flag

    # 3️⃣ Dust logic with ML validation
    if vision_label == "Dust":
        if loss_percent > LOSS_THRESHOLD:
            if rain_expected:
                return "🕒 Postpone Cleaning - Rain Expected", dust_flag
            return "🧹 Cleaning Required - Dust Detected", dust_flag
        else:
            return "⚠️ Dust Detected - Loss Below Threshold (Monitor)", dust_flag

    # 4️⃣ Clean panels
    return "✅ System Healthy", dust_flag
