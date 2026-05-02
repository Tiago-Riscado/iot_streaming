# IoT Real-time Streaming Dashboard

Simulated IoT sensor pipeline with real-time aggregation, temperature alerting, and live visualisation — available in two modes.

## Structure

```
iot-streaming/
│
├── app.py              # Streamlit web dashboard
├── terminal.py         # Terminal pipeline with Streamz + live matplotlib
│
├── src/
│   ├── config.py       # All constants and env vars
│   ├── simulator.py    # IoT event generator (with anomaly spikes)
│   ├── pipeline.py     # Aggregation logic + AlertManager
│   └── plots.py        # Shared matplotlib chart functions
│
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env    # adjust parameters if needed
```

## Usage

```bash
# Web dashboard (Streamlit)
streamlit run app.py

# Terminal pipeline (Streamz + matplotlib)
python terminal.py
```

## Configuration (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `EMIT_INTERVAL` | `0.5` | Seconds between events |
| `WINDOW_SIZE` | `5` | Events per aggregation window |
| `TOTAL_SIMULATION_STEPS` | `200` | Total events to simulate |
| `TEMP_ALERT_LIMIT` | `26.5` | Temperature threshold for alerts (°C) |
| `ALERT_DEBOUNCE_SECONDS` | `10` | Minimum seconds between alerts |

## Features

- Simulated sensors (A/B/C/D) with random anomaly spikes (5% probability)
- Windowed aggregation: avg temperature, humidity, energy per window
- Debounced alerts: WARNING (>26.5°C) and CRITICAL (>28.5°C)
- Live trend charts: temperature / humidity / energy over time
- Energy vs Temperature scatter plot
