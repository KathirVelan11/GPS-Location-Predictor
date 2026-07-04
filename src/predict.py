"""Predict a patient's location from a date and time using a trained model.

Usage:
    python src/predict.py --datetime "2024-05-20 15:51:00"
    python src/predict.py --datetime "2024-05-20 15:51:00" --model models/model.joblib
"""
from __future__ import annotations

import argparse

import joblib
import pandas as pd

from preprocessing import FEATURE_COLUMNS, build_features


def predict(dt_string: str, model_path: str = "models/model.joblib"):
    bundle = joblib.load(model_path)
    model = bundle["model"]

    dt = pd.to_datetime(dt_string, dayfirst=False)
    df = pd.DataFrame({"lat": [0.0], "lon": [0.0], "datetime": [dt]})
    feats = build_features(df)[FEATURE_COLUMNS].values
    lat, lon = model.predict(feats)[0]
    return float(lat), float(lon)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datetime", required=True, help='e.g. "2024-05-20 15:51:00"')
    ap.add_argument("--model", default="models/model.joblib")
    args = ap.parse_args()
    lat, lon = predict(args.datetime, args.model)
    print(f"Input     : {args.datetime}")
    print(f"Predicted : Latitude {lat:.6f}, Longitude {lon:.6f}")
    print(f"Map       : https://www.google.com/maps?q={lat:.6f},{lon:.6f}")


if __name__ == "__main__":
    main()
