"""
Streamlit IoT Dashboard — real-time simulation with alerts and trend charts.

Run:
    streamlit run app.py
"""

import time
import pandas as pd
import streamlit as st

from src.config    import EMIT_INTERVAL, WINDOW_SIZE, TOTAL_SIMULATION_STEPS
from src.simulator import generate_iot_event
from src.pipeline  import aggregate, AlertManager
from src.plots     import plot_trends, plot_scatter


# ------------------------------------------------------------------ #
# Session state initialisation
# ------------------------------------------------------------------ #

def _init():
    defaults = {
        "raw_window":    [],
        "data_history":  [],
        "running":       False,
        "sim_step":      0,
        "alert_manager": AlertManager(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ------------------------------------------------------------------ #
# Data processing
# ------------------------------------------------------------------ #

def process_step():
    st.session_state.raw_window.append(generate_iot_event())
    st.session_state.sim_step += 1

    if len(st.session_state.raw_window) >= WINDOW_SIZE:
        window   = st.session_state.raw_window[:WINDOW_SIZE]
        agg      = aggregate(window)
        alert    = st.session_state.alert_manager.check(agg)
        st.session_state.data_history.append(agg)
        st.session_state.raw_window = st.session_state.raw_window[WINDOW_SIZE:]
        return agg, alert

    return None, None


# ------------------------------------------------------------------ #
# Rendering
# ------------------------------------------------------------------ #

def render(alert_ph, table_ph):
    if not st.session_state.data_history:
        st.write("Waiting for data…")
        return

    df   = pd.DataFrame(st.session_state.data_history)
    last = df.iloc[-1]
    am   = st.session_state.alert_manager

    with table_ph.container():
        st.subheader("Latest Aggregation")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Temperature (°C)", f"{last['avg_temp']:.2f}")
        c2.metric("Avg Humidity (%)",      f"{last['avg_hum']:.2f}")
        c3.metric("Avg Energy",            f"{last['avg_energy']:.2f}")
        c4.metric("Event Count",           last["count"])

        st.dataframe(
            df.tail(5).sort_values("window_end", ascending=False),
            use_container_width=True, hide_index=True,
            column_order=["window_end", "avg_temp", "avg_hum", "avg_energy", "count", "sources"],
        )

    if am.alerts_history:
        df_alerts = pd.DataFrame(am.alerts_history).sort_values("timestamp", ascending=False)
        last_alert = df_alerts.iloc[0]
        with alert_ph.container():
            msg = f"**{last_alert['level']}** | {last_alert['timestamp'].strftime('%H:%M:%S')} | Temp: {last_alert['avg_temp']:.2f}°C"
            (st.error if last_alert["level"] == "CRITICAL" else st.warning)(msg)
            with st.expander("Alert History"):
                st.dataframe(df_alerts, use_container_width=True, hide_index=True)
    else:
        alert_ph.info("✅ All clear. No temperature alerts.")

    st.subheader("Real-time Trends")
    st.pyplot(plot_trends(df))

    st.subheader("Energy vs Temperature")
    st.pyplot(plot_scatter(df))


# ------------------------------------------------------------------ #
# Layout
# ------------------------------------------------------------------ #

st.set_page_config(layout="wide", page_title="IoT Real-time Dashboard")
st.title("IoT Monitoring System (Simulation)")

alert_ph = st.empty()
table_ph = st.empty()

if st.session_state.running:
    if st.button("Pause Simulation"):
        st.session_state.running = False
        st.rerun()
else:
    if st.button("Start Simulation"):
        st.session_state.running = True
        st.rerun()

progress_bar = st.progress(0)
status_text  = st.empty()

# ------------------------------------------------------------------ #
# Main loop
# ------------------------------------------------------------------ #

if st.session_state.running and st.session_state.sim_step < TOTAL_SIMULATION_STEPS:
    process_step()
    render(alert_ph, table_ph)
    progress_bar.progress(st.session_state.sim_step / TOTAL_SIMULATION_STEPS)
    status_text.text(f"Step: {st.session_state.sim_step} / {TOTAL_SIMULATION_STEPS}")
    time.sleep(EMIT_INTERVAL)
    st.rerun()

elif st.session_state.running and st.session_state.sim_step >= TOTAL_SIMULATION_STEPS:
    st.session_state.running = False
    progress_bar.progress(1.0)
    status_text.success("Simulation complete!")
    render(alert_ph, table_ph)

elif not st.session_state.running and st.session_state.sim_step > 0:
    status_text.info("Simulation paused.")
    render(alert_ph, table_ph)

else:
    status_text.write("Press 'Start Simulation' to begin.")
