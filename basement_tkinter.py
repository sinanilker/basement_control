import tkinter as tk
from tkinter import messagebox, ttk

def evaluate():
    try:
        co2 = float(co2_entry.get())
        humidity = float(humidity_entry.get())
        aqi = int(aqi_entry.get())
        lux = float(lux_entry.get())
        presence = presence_var.get()

        scenario = scenario_var.get()
        if not scenario:
            messagebox.showerror("Error", "Please select a scenario.")
            return

        # --- Window Logic Thresholds ---
        # CO₂ < 600 ppm        → closed
        # 600 ≤ CO₂ < 800 ppm  → monitor and prepare to open
        # 800 ≤ CO₂ ≤ 1000 ppm → partially open
        # CO₂ > 1000 ppm       → fully open
        # Window logic
        if co2 < 600:
            window = "closed"
        elif 600 <= co2 < 800:
            window = "monitor and prepare to open"
        elif 800 <= co2 <= 1000:
            window = "partially open"
        else:
            window = "fully open"

        # --- Ventilation Logic Thresholds ---
        # AQI > 150        → strong fresh air flush
        # 100 ≤ AQI ≤ 150  → fresh air flush
        # Humidity > 60%   → dehumidify mode
        # Humidity < 30%   → humidify mode
        # Otherwise        → normal
        # Ventilation logic
        if aqi > 150:
            ventilation = "strong fresh air flush"
        elif 100 <= aqi <= 150:
            ventilation = "fresh air flush"
        elif humidity > 60:
            ventilation = "dehumidify mode"
        elif humidity < 30:
            ventilation = "humidify mode"
        else:
            ventilation = "normal"

        # --- Lighting Logic by Scenario and Lux ---
        # Lux < 100        → low lighting
        # 100 ≤ Lux ≤ 300  → mid lighting
        # Lux > 300        → off or minimal depending on scenario
        #
        # Scenario-specific behavior:
        # Empty       → corridor ambient lighting
        # Exhibition  → wall + ambient lighting
        # Maintenance → task lights
        # Workshop    → central + wall task lights
        # Lounge      → warm ambient + study spotlights
        # Lighting logic
        lighting = "off"
        if scenario == "0. Empty":
            if lux < 100:
                lighting = "corridor ambient lighting (low)"
            elif 100 <= lux <= 300:
                lighting = "corridor ambient lighting (mid)"
        elif scenario == "1. Exhibition":
            lighting = "wall + ambient (low)" if lux < 100 else "wall + ambient (mid)" if lux <= 300 else "off"
        elif scenario == "2. Maintenance":
            lighting = "task lights (low)" if lux < 100 else "task lights (mid)" if lux <= 300 else "off"
        elif scenario == "3. Workshop":
            lighting = "central + wall task lighting (low)" if lux < 100 else "central lighting only (mid)" if lux <= 300 else "off"
        elif scenario == "4. Lounge":
            lighting = "warm ambient + study spotlights (mood)" if lux < 100 else "ambient only" if lux <= 300 else "minimal"

        # Report
        result = f"""--- Sensor & Selection Report ---
Scenario: {scenario}
CO₂: {co2} ppm
Humidity: {humidity}% RH
AQI: {aqi}
Lux: {lux}
Presence: {'Yes' if presence else 'No'}

--- Final Control Decisions ---
Window: {window}
Lighting: {lighting}
Ventilation: {ventilation}
"""
        result += "\nSystem Note: After this scenario ends, the system will enter Maintenance mode for 1 hour, then switch to Empty mode until the next reservation or override."
        messagebox.showinfo("Control Results", result)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

def add_placeholder(entry, placeholder_text):
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg='gray')
    entry.insert(0, placeholder_text)
    entry.config(fg='gray')
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# GUI setup
root = tk.Tk()
root.title("Basement Control System")

tk.Label(root, text="Select Scenario", anchor="w").grid(row=0, column=0, sticky="w")
scenario_var = tk.StringVar()
ttk.Combobox(root, textvariable=scenario_var, values=["0. Empty", "1. Exhibition", "2. Maintenance", "3. Workshop", "4. Lounge"]).grid(row=0, column=1)

tk.Label(root, text="CO₂ (ppm)", anchor="w").grid(row=1, column=0, sticky="w")
co2_entry = tk.Entry(root)
co2_entry.grid(row=1, column=1)

tk.Label(root, text="Humidity (%RH)", anchor="w").grid(row=2, column=0, sticky="w")
humidity_entry = tk.Entry(root)
humidity_entry.grid(row=2, column=1)

tk.Label(root, text="Air Quality Index (AQI)", anchor="w").grid(row=3, column=0, sticky="w")
aqi_entry = tk.Entry(root)
aqi_entry.grid(row=3, column=1)

tk.Label(root, text="Indoor Light (lux)", anchor="w").grid(row=4, column=0, sticky="w")
lux_entry = tk.Entry(root)
lux_entry.grid(row=4, column=1)

tk.Label(root, text="Presence Detected?", anchor="w").grid(row=5, column=0, sticky="w")
presence_var = tk.BooleanVar()
tk.Checkbutton(root, text="Yes", variable=presence_var).grid(row=5, column=1)

tk.Button(root, text="Evaluate Control Decision", command=evaluate).grid(row=6, columnspan=2, pady=10)

add_placeholder(co2_entry, "e.g. 1200")
add_placeholder(humidity_entry, "e.g. 45")
add_placeholder(aqi_entry, "e.g. 80")
add_placeholder(lux_entry, "e.g. 150")

root.mainloop()