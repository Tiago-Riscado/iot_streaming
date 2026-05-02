import random
from datetime import datetime
from src.config import IDEAL_TEMP, SENSOR_IDS, ANOMALY_PROB


def generate_iot_event() -> dict:
    """
    Generates a single simulated IoT sensor event.
    Includes a small probability of an anomalous temperature spike.
    """
    timestamp   = datetime.now()
    origin      = random.choice(SENSOR_IDS)
    temperature = round(IDEAL_TEMP + random.uniform(-2, 3), 2)

    # Random anomaly spike
    if random.random() < ANOMALY_PROB:
        temperature += random.uniform(3, 8)

    temperature = round(temperature, 2)
    energy      = round(5 + abs(temperature - IDEAL_TEMP) + random.uniform(0, 2), 2)
    humidity    = round(65 - (temperature - IDEAL_TEMP) * 2 + random.uniform(-5, 5), 2)
    humidity    = max(0.0, min(100.0, humidity))

    return {
        "timestamp":          timestamp,
        "origin":             origin,
        "temperature":        temperature,
        "humidity":           humidity,
        "energy_consumption": energy,
    }
