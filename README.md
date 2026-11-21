# IoT-Based Smart Home Monitoring Dashboard

## Project status and scope
This repository contains a dataset-backed dashboard for the HCLTech Career Shaper Programme project. It analyses the supplied `dataset.csv` and provides room, sensor, environmental and alert views.

**Important:** this version is a software demonstration using the supplied CSV. It is not connected to an ESP32, physical sensors, relay hardware, MQTT broker, or a live Blynk account. Do not describe it as a physical/live IoT deployment unless those components are subsequently implemented and tested.

## Dataset
The supplied CSV has 5,000 rows and these 8 columns:
- `timestamp`
- `device_id`
- `sensor_type`
- `room`
- `temperature_C`
- `humidity_pct`
- `value`
- `alert_flag`

The generic `value` field is sensor-dependent; its unit is not defined in the supplied report. The `alert_flag` is treated as a supplied label, not independently verified ground truth.

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Files
- `app.py` — interactive Streamlit dashboard.
- `dataset.csv` — supplied project dataset.
- `requirements.txt` — Python dependencies.
- `eda_analysis.py` — reproducible descriptive analysis and chart generation.
- `data_dictionary.csv` — column descriptions and caveats.
- `ETHICS_AND_LIMITATIONS.md` — provenance, privacy and implementation status.

## GitHub upload
Create a new public or private GitHub repository, for example `iot-smart-home-automation`. Upload all files in this folder. The repository URL can then be added to the project portal. Do not invent a repository URL before creating it.

## Dashboard deployment
The dashboard can be deployed on Streamlit Community Cloud after pushing this folder to GitHub. Select `app.py` as the main file. A deployed URL is only available after successful deployment.

## Validation
The dashboard validates required columns, parses timestamps, coerces numeric fields, filters invalid timestamps, and supports room, sensor and date filters. It does not establish sensor accuracy, command latency, MQTT delivery, hardware uptime, or alert precision/recall.
