"""Load and feature-engineer the GPS log.

This is a cleaned-up, importable version of the feature engineering that
originally lived in the exploratory notebook. Two correctness fixes over the
notebook version:

1. No blanket ``np.log1p`` over the whole feature matrix. The notebook applied
   log1p to one-hot and sin/cos columns too -- log1p of a value <= -1 (which
   Time_cos can reach) is undefined and silently produces NaN/-inf. Here only
   the strictly-positive continuous columns are considered for scaling, and
   scaling is handled by the model pipeline instead.
2. Latitude/longitude are kept as plain regression targets. The N/S/E/W
   direction flags are constant for this deployment region and add no signal,
   so they are dropped rather than "predicted".
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "Days_from_ref",
    "Seconds_from_midnight",
    "HourOfDay",
    "DayOfWeek",
    "IsWeekend",
    "Morning",
    "Afternoon",
    "Evening",
    "Night",
    "Time_sin",
    "Time_cos",
    "Day_sin",
    "Day_cos",
]
TARGET_COLUMNS = ["lat", "lon"]
REFERENCE_DATE = pd.Timestamp("1900-01-01")


def load_raw(csv_path: str) -> pd.DataFrame:
    """Read the raw logger CSV and normalise its messy column names/values."""
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={"Lat": "lat", "Long": "lon"})

    # The logger writes 0.0 / '-' / '0/0/0' for fixes it could not resolve.
    df["lat"] = df["lat"].replace(0, np.nan)
    df["lon"] = df["lon"].replace(0, np.nan)
    df[["lat", "lon"]] = df[["lat", "lon"]].ffill()

    df["Date"] = df["Date"].replace("-", np.nan)
    df["Time"] = df["Time"].replace("-", np.nan)
    df = df.dropna(subset=["Date", "Time"])
    df = df[~((df["Date"] == "0/0/0") & (df["Time"] == "0:0:0"))]

    df["datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"], dayfirst=True, errors="coerce"
    )
    df = df.dropna(subset=["datetime", "lat", "lon"]).reset_index(drop=True)
    return df.sort_values("datetime").reset_index(drop=True)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive temporal features from the ``datetime`` column."""
    dt = df["datetime"]
    secs = dt.dt.hour * 3600 + dt.dt.minute * 60 + dt.dt.second
    hour = dt.dt.hour
    dow = dt.dt.dayofweek

    out = pd.DataFrame(index=df.index)
    out["Days_from_ref"] = (dt.dt.normalize() - REFERENCE_DATE).dt.days
    out["Seconds_from_midnight"] = secs
    out["HourOfDay"] = hour
    out["DayOfWeek"] = dow
    out["IsWeekend"] = (dow >= 5).astype(int)
    out["Morning"] = ((hour >= 6) & (hour < 12)).astype(int)
    out["Afternoon"] = ((hour >= 12) & (hour < 18)).astype(int)
    out["Evening"] = ((hour >= 18) & (hour < 21)).astype(int)
    out["Night"] = ((hour >= 21) | (hour < 6)).astype(int)
    # Cyclical encodings so 23:59 is "close to" 00:00 and Sun close to Mon.
    out["Time_sin"] = np.sin(2 * np.pi * secs / 86400)
    out["Time_cos"] = np.cos(2 * np.pi * secs / 86400)
    out["Day_sin"] = np.sin(2 * np.pi * dow / 7)
    out["Day_cos"] = np.cos(2 * np.pi * dow / 7)

    out["lat"] = df["lat"].values
    out["lon"] = df["lon"].values
    out["datetime"] = df["datetime"].values
    return out


def load_dataset(csv_path: str) -> pd.DataFrame:
    """Full path: raw CSV -> engineered feature frame."""
    return build_features(load_raw(csv_path))
