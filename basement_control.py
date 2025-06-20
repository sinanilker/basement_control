def basement_control():
    print("Welcome to the Basement Environment Control System!")
    print("Getting the data from TISS Reservation System TU Wien;")
    
    scenarios = {
        "0": "Empty",
        # Checks the co2 level; if there are people, it lights up the corridors.
        "1": "Exhibition",
        # Paintings and artifacts on display; specific lighting and humidity control.
        "2": "Maintenance",
        # Workers present; general task lighting and ventilation.
        "3": "Workshop",
        # Focused task lighting; air quality and humidity control.
        "4": "Lounge"
        # Soft lighting for relaxing or studying; full environmental control.
    }
    
    print("\nAvailable Scenarios:")
    for key, value in scenarios.items():
        print(f"{key}: {value}")

    while True:
        scenario_choice = input("\nOverride the data and enter the number for the current scenario: ").strip()
        if scenario_choice in scenarios:
            scenario = scenarios[scenario_choice]
            break
        print("Invalid scenario selected. Please enter a valid number!")
    print(f"\nScenario selected: {scenario}")
    
    while True:
        try:
            co2_level = float(input("CO₂ (ppm) – MH-Z19 sensor: ").strip())
            humidity  = float(input("Humidity (%RH) – DHT22 sensor: ").strip())
            aqi       = int(input("Air Quality Index – PMS5003 sensor: ").strip())
            lux_level = float(input("Indoor illuminance (lux) – TSL2591 sensor: ").strip())
            break
        except ValueError:
            print("Invalid sensor data input. Please enter numerical values.")
    
    while True:
        presence_input = input("Presence detected? (y/n): ").strip().lower()
        if presence_input in ("y", "n"):
            presence_detected = (presence_input == "y")
            break
        print("Invalid input. Please enter 'y' or 'n'.")
    
    window_action = "closed"
    lighting_action = "off"
    ventilation_action = "normal"

    # Updated CO₂ threshold logic
    if co2_level < 600:
        window_action = "closed"
    elif 600 <= co2_level < 800:
        window_action = "monitor and prepare to open"
    elif 800 <= co2_level <= 1000:
        window_action = "partially open"
    else:
        window_action = "fully open"

    if humidity > 60:
        ventilation_action = "dehumidify mode"
    elif humidity < 30:
        ventilation_action = "humidify mode"
    else:
        ventilation_action = "normal"

    # Updated AQI threshold logic
    if aqi > 150:
        ventilation_action = "strong fresh air flush"
    elif 100 <= aqi <= 150:
        ventilation_action = "fresh air flush"
    else:
        ventilation_action = "normal"

    # Unified Lighting Control Logic
    if scenario == "Empty":
        if lux_level < 100:
            lighting_action = "corridor ambient lighting (low)"
        elif 100 <= lux_level <= 300:
            lighting_action = "corridor ambient lighting (mid)"
        else:
            lighting_action = "off"

    elif scenario == "Exhibition":
        if lux_level < 100:
            lighting_action = "wall + ambient (low)"
        elif 100 <= lux_level <= 300:
            lighting_action = "wall + ambient (mid)"
        else:
            lighting_action = "off"

    elif scenario == "Maintenance":
        if lux_level < 100:
            lighting_action = "task lights (low)"
        elif 100 <= lux_level <= 300:
            lighting_action = "task lights (mid)"
        else:
            lighting_action = "off"

    elif scenario == "Workshop":
        if lux_level < 100:
            lighting_action = "central + wall task lighting (low)"
        elif 100 <= lux_level <= 300:
            lighting_action = "central lighting only (mid)"
        else:
            lighting_action = "off"

    elif scenario == "Lounge":
        if lux_level < 100:
            lighting_action = "warm ambient + study spotlights (mood)"
        elif 100 <= lux_level <= 300:
            lighting_action = "ambient only"
        else:
            lighting_action = "minimal"

    # Summary report of selections and sensor inputs
    print("\n--- Sensor & Selection Report ---")
    print(f"Scenario: {scenario}")
    print(f"Indoor Lux Level: {lux_level} lux")
    print(f"CO₂ Level: {co2_level} ppm")
    print(f"Humidity: {humidity}%RH")
    print(f"AQI: {aqi}")
    print(f"Presence Detected: {'Yes' if presence_detected else 'No'}")

    print("\n--- Final Control Decisions ---")
    print(f"Window action: {window_action}")
    print(f"Lighting action: {lighting_action}")
    print(f"Ventilation action: {ventilation_action}")
    print("-------------------------------")
    print("After the scenario slot ends, wait 1 hour in Maintenance mode, then switch to Empty mode until the next reservation or an override.")
    
if __name__ == "__main__":
    basement_control()