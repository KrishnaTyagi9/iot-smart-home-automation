import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="IoT Smart Home Monitoring", page_icon="🏠", layout="wide")

DATA_PATH = Path(__file__).parent / "dataset.csv"
REQUIRED = {
    "timestamp", "device_id", "sensor_type", "room",
    "temperature_C", "humidity_pct", "value", "alert_flag"
}

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    for col in ["temperature_C", "humidity_pct", "value", "alert_flag"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    return df

df = load_data()
st.title("🏠 IoT-Based Smart Home Monitoring Dashboard")
st.caption("Dataset-backed demonstration • This dashboard visualises the supplied CSV; it is not connected to physical sensors or a live MQTT broker.")

with st.sidebar:
    st.header("Filters")
    rooms = sorted(df["room"].dropna().unique().tolist())
    selected_rooms = st.multiselect("Room", rooms, default=rooms)
    sensors = sorted(df["sensor_type"].dropna().unique().tolist())
    selected_sensors = st.multiselect("Sensor type", sensors, default=sensors)
    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    st.divider()
    st.markdown("**Data source**")
    st.write("`dataset.csv`")
    st.write(f"{len(df):,} source records")

filtered = df[df["room"].isin(selected_rooms) & df["sensor_type"].isin(selected_sensors)].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start = pd.Timestamp(date_range[0])
    end = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    filtered = filtered[filtered["timestamp"].between(start, end)]

if filtered.empty:
    st.warning("No records match the selected filters. Change the filters to see results.")
    st.stop()

total = len(filtered)
alerts = int((filtered["alert_flag"] == 1).sum())
c1, c2, c3, c4 = st.columns(4)
c1.metric("Records", f"{total:,}")
c2.metric("Devices", f"{filtered['device_id'].nunique():,}")
c3.metric("Alert-labelled records", f"{alerts:,}")
c4.metric("Alert-labelled share", f"{alerts / total * 100:.2f}%")

st.info("Interpretation note: `alert_flag` is a supplied dataset label. Its rule and ground truth have not been independently verified. The generic `value` field is sensor-specific and has no common unit defined in the source report.")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Environment", "Alerts", "Raw data"])

with tab1:
    left, right = st.columns(2)
    with left:
        counts = filtered["room"].value_counts().rename_axis("Room").reset_index(name="Records")
        st.plotly_chart(px.bar(counts, x="Room", y="Records", title="Records by room"), use_container_width=True)
    with right:
        sensor_counts = filtered["sensor_type"].value_counts().rename_axis("Sensor type").reset_index(name="Records")
        st.plotly_chart(px.bar(sensor_counts, x="Sensor type", y="Records", title="Records by sensor type"), use_container_width=True)
    daily = filtered.set_index("timestamp").resample("D")["temperature_C"].mean().reset_index()
    st.plotly_chart(px.line(daily, x="timestamp", y="temperature_C", title="Daily mean temperature", labels={"timestamp":"Date", "temperature_C":"Temperature (°C)"}), use_container_width=True)

with tab2:
    left, right = st.columns(2)
    with left:
        st.plotly_chart(px.histogram(filtered, x="temperature_C", nbins=25, title="Temperature distribution", labels={"temperature_C":"Temperature (°C)"}), use_container_width=True)
    with right:
        st.plotly_chart(px.histogram(filtered, x="humidity_pct", nbins=25, title="Humidity distribution", labels={"humidity_pct":"Relative humidity (%)"}), use_container_width=True)
    st.write("Descriptive statistics")
    st.dataframe(filtered[["temperature_C", "humidity_pct", "value"]].describe().T, use_container_width=True)

with tab3:
    by_room = filtered.groupby("room", as_index=False).agg(records=("alert_flag","size"), alert_records=("alert_flag","sum"))
    by_room["alert_share_pct"] = (by_room["alert_records"] / by_room["records"] * 100).round(2)
    st.plotly_chart(px.bar(by_room, x="room", y="alert_records", title="Alert-labelled records by room"), use_container_width=True)
    st.dataframe(by_room, use_container_width=True)
    alert_rows = filtered[filtered["alert_flag"] == 1].sort_values("timestamp", ascending=False)
    st.subheader("Alert-labelled records")
    st.dataframe(alert_rows, use_container_width=True)

with tab4:
    st.dataframe(filtered, use_container_width=True, height=420)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_smart_home_data.csv", "text/csv")

st.divider()
st.caption(f"Displayed {total:,} of {len(df):,} records after filtering. Dashboard refreshes when filters change; no live device telemetry is being received.")
