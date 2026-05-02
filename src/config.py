import os
from dotenv import load_dotenv

load_dotenv()

# Simulation
EMIT_INTERVAL          = float(os.getenv("EMIT_INTERVAL",          0.5))
WINDOW_SIZE            = int(os.getenv("WINDOW_SIZE",               5))
TOTAL_SIMULATION_STEPS = int(os.getenv("TOTAL_SIMULATION_STEPS",    200))

# Thresholds
TEMP_ALERT_LIMIT       = float(os.getenv("TEMP_ALERT_LIMIT",        26.5))
IDEAL_TEMP             = float(os.getenv("IDEAL_TEMP",              25.0))
ALERT_DEBOUNCE_SECONDS = int(os.getenv("ALERT_DEBOUNCE_SECONDS",    10))

# Sensors
SENSOR_IDS = ["Sensor_A", "Sensor_B", "Sensor_C", "Sensor_D"]
ANOMALY_PROB  = 0.05   # probability of a random temperature spike
