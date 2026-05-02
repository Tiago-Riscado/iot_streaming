"""
Terminal IoT Pipeline — uses Streamz for streaming, prints aggregations
to stdout and shows a live matplotlib chart.

Run:
    python terminal.py
"""

import time
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tabulate import tabulate
from streamz import Stream

from src.config    import EMIT_INTERVAL, WINDOW_SIZE, TOTAL_SIMULATION_STEPS
from src.simulator import generate_iot_event
from src.pipeline  import aggregate, AlertManager
from src.plots     import plot_scatter

# ------------------------------------------------------------------ #
# Shared state
# ------------------------------------------------------------------ #

data_history: list[dict] = []
alert_manager = AlertManager()

# ------------------------------------------------------------------ #
# Pipeline steps
# ------------------------------------------------------------------ #

def enrich(event: dict) -> dict:
    event["valid"] = True
    return event

def is_valid(event: dict) -> bool:
    return event.get("valid", False)

def process_aggregation(agg: dict) -> dict:
    alert = alert_manager.check(agg)
    if alert:
        print(f"\n[{alert['level']}] {alert['timestamp'].strftime('%H:%M:%S')} — "
              f"Avg Temp: {alert['avg_temp']:.2f}°C (limit: {alert['limit']}°C)\n", flush=True)
    data_history.append(agg)
    print(tabulate([agg], headers="keys", tablefmt="github",
                   showindex=False, floatfmt=".2f"), flush=True)
    return agg

# ------------------------------------------------------------------ #
# Streamz pipeline
# ------------------------------------------------------------------ #

source   = Stream()
pipeline = (
    source
    .map(enrich)
    .filter(is_valid)
    .partition(WINDOW_SIZE)
    .map(aggregate)
    .map(process_aggregation)
)

# ------------------------------------------------------------------ #
# Simulation thread
# ------------------------------------------------------------------ #

def run_simulation():
    for _ in range(TOTAL_SIMULATION_STEPS):
        source.emit(generate_iot_event())
        time.sleep(EMIT_INTERVAL)

threading.Thread(target=run_simulation, daemon=True).start()

# ------------------------------------------------------------------ #
# Live matplotlib chart
# ------------------------------------------------------------------ #

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

def animate(_):
    if not data_history:
        return
    recent  = data_history[-40:]
    times   = [a["window_end"].strftime("%H:%M:%S") for a in recent]
    temps   = [a["avg_temp"]   for a in recent]
    hums    = [a["avg_hum"]    for a in recent]
    energies = [a["avg_energy"] for a in recent]

    for ax in (ax1, ax2, ax3):
        ax.clear()

    from src.config import TEMP_ALERT_LIMIT
    ax1.plot(times, temps,    marker="o", color="tab:blue",   label="Avg Temp (°C)")
    ax1.axhline(TEMP_ALERT_LIMIT, linestyle="--", color="r", label=f"Limit ({TEMP_ALERT_LIMIT}°C)")
    ax1.set_ylabel("Temperature (°C)"); ax1.legend(loc="upper left"); ax1.grid(True)

    ax2.plot(times, hums,     marker="x", color="tab:orange", label="Avg Humidity (%)")
    ax2.set_ylabel("Humidity (%)"); ax2.legend(loc="upper left"); ax2.grid(True)

    ax3.plot(times, energies, marker="s", color="tab:green",  label="Avg Energy")
    ax3.set_ylabel("Energy"); ax3.set_xlabel("Time")
    ax3.legend(loc="upper left"); ax3.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()

ani = FuncAnimation(fig, animate, interval=200)
plt.show()

# ------------------------------------------------------------------ #
# Final scatter plot (after simulation ends)
# ------------------------------------------------------------------ #

if data_history:
    import pandas as pd
    st_fig = plot_scatter(pd.DataFrame(data_history))
    plt.show()
