from datetime import datetime
import pandas as pd
from src.config import TEMP_ALERT_LIMIT, ALERT_DEBOUNCE_SECONDS


def aggregate(window: list) -> dict:
    """Aggregates a window of raw events into summary statistics."""
    df = pd.DataFrame(window)
    return {
        "window_end": df["timestamp"].max(),
        "avg_temp":   round(df["temperature"].mean(),          2),
        "avg_hum":    round(df["humidity"].mean(),             2),
        "avg_energy": round(df["energy_consumption"].mean(),   2),
        "count":      len(df),
        "sources":    ",".join(sorted(df["origin"].unique())),
    }


class AlertManager:
    """
    Stateful alert manager with debounce logic.
    Shared between the Streamlit dashboard and the terminal pipeline.
    """

    def __init__(self):
        self.alert_last    = datetime.min
        self.alerts_history: list[dict] = []

    def check(self, agg: dict) -> dict | None:
        """
        Returns an alert dict if the aggregated temperature exceeds the limit
        and the debounce window has passed. Otherwise returns None.
        """
        now = datetime.now()
        if (now - self.alert_last).total_seconds() < ALERT_DEBOUNCE_SECONDS:
            return None

        if agg["avg_temp"] > TEMP_ALERT_LIMIT:
            level = "CRITICAL" if agg["avg_temp"] > TEMP_ALERT_LIMIT + 2 else "WARNING"
            alert = {
                "timestamp": now,
                "level":     level,
                "avg_temp":  agg["avg_temp"],
                "limit":     TEMP_ALERT_LIMIT,
            }
            self.alert_last = now
            self.alerts_history.append(alert)
            return alert

        return None
