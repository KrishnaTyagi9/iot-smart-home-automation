from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
df = pd.read_csv(ROOT / "dataset.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
OUT = ROOT / "eda_outputs"
OUT.mkdir(exist_ok=True)

print("Shape:", df.shape)
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nNumeric summary:\n", df[["temperature_C","humidity_pct","value"]].describe())
print("\nAlert counts:\n", df["alert_flag"].value_counts(dropna=False))
print("\nRoom counts:\n", df["room"].value_counts())

fig, ax = plt.subplots()
df["temperature_C"].hist(bins=25, ax=ax)
ax.set(title="Temperature distribution", xlabel="Temperature (°C)", ylabel="Records")
fig.tight_layout(); fig.savefig(OUT / "temperature_distribution.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots()
df["humidity_pct"].hist(bins=25, ax=ax)
ax.set(title="Humidity distribution", xlabel="Relative humidity (%)", ylabel="Records")
fig.tight_layout(); fig.savefig(OUT / "humidity_distribution.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots()
df["room"].value_counts().plot(kind="bar", ax=ax)
ax.set(title="Records by room", xlabel="Room", ylabel="Records")
fig.tight_layout(); fig.savefig(OUT / "records_by_room.png", dpi=160); plt.close(fig)

daily = df.set_index("timestamp").resample("D")["temperature_C"].mean()
fig, ax = plt.subplots()
daily.plot(ax=ax)
ax.set(title="Daily mean temperature", xlabel="Date", ylabel="Temperature (°C)")
fig.tight_layout(); fig.savefig(OUT / "daily_mean_temperature.png", dpi=160); plt.close(fig)

print(f"\nCharts saved in {OUT}")
