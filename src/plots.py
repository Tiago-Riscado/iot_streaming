import matplotlib.pyplot as plt
import pandas as pd
from src.config import TEMP_ALERT_LIMIT


def plot_trends(df: pd.DataFrame):
    """
    Renders a 3-panel time-series chart:
    Temperature / Humidity / Energy consumption.
    Returns the matplotlib Figure.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    ax1.plot(df["window_end"], df["avg_temp"],   marker="o", linestyle="-",  color="tab:blue",   label="Avg Temp (°C)")
    ax1.axhline(TEMP_ALERT_LIMIT, linestyle="--", color="r", label=f"Limit ({TEMP_ALERT_LIMIT}°C)")
    ax1.set_ylabel("Temperature (°C)")
    ax1.legend(loc="upper left"); ax1.grid(True)

    ax2.plot(df["window_end"], df["avg_hum"],    marker="x", linestyle="--", color="tab:orange", label="Avg Humidity (%)")
    ax2.set_ylabel("Humidity (%)")
    ax2.legend(loc="upper left"); ax2.grid(True)

    ax3.plot(df["window_end"], df["avg_energy"], marker="s", linestyle=":",  color="tab:green",  label="Avg Energy")
    ax3.set_ylabel("Energy"); ax3.set_xlabel("Time")
    ax3.legend(loc="upper left"); ax3.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_scatter(df: pd.DataFrame):
    """Energy vs Temperature scatter plot. Returns the matplotlib Figure."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["avg_temp"], df["avg_energy"], color="tab:green", alpha=0.6)
    ax.set_xlabel("Avg Temperature (°C)")
    ax.set_ylabel("Avg Energy")
    ax.set_title("Energy vs Temperature")
    ax.grid(True)
    plt.tight_layout()
    return fig
