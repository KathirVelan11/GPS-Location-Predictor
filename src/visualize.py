"""Visualise actual vs. predicted locations.

Produces two artefacts:
  * examples/predictions.png  -- a static scatter (embeddable in the README)
  * examples/map.html         -- an interactive Folium map

Usage:
    python src/visualize.py --data data/sample_gps.csv --model models/model.joblib
"""
from __future__ import annotations

import argparse
import os

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from preprocessing import FEATURE_COLUMNS, TARGET_COLUMNS, load_dataset
from train import time_split


def make_plots(data_path, model_path, out_dir="examples"):
    os.makedirs(out_dir, exist_ok=True)
    bundle = joblib.load(model_path)
    model = bundle["model"]

    df = load_dataset(data_path)
    _, test_df = time_split(df)
    y_true = test_df[TARGET_COLUMNS].values
    y_pred = model.predict(test_df[FEATURE_COLUMNS].values)

    # --- static scatter for the README ---
    plt.figure(figsize=(7, 6))
    plt.scatter(y_true[:, 1], y_true[:, 0], s=18, alpha=0.6,
                label="Actual", color="#2c7fb8")
    plt.scatter(y_pred[:, 1], y_pred[:, 0], s=18, alpha=0.6,
                label="Predicted", color="#de2d26", marker="x")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Actual vs. Predicted patient locations (held-out test days)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    png = os.path.join(out_dir, "predictions.png")
    plt.savefig(png, dpi=120)
    plt.close()

    # --- interactive Folium map ---
    try:
        import folium
        center = [float(y_true[:, 0].mean()), float(y_true[:, 1].mean())]
        fmap = folium.Map(location=center, zoom_start=15)
        for lat, lon in y_true:
            folium.CircleMarker([lat, lon], radius=3, color="#2c7fb8",
                                fill=True, popup="actual").add_to(fmap)
        for lat, lon in y_pred:
            folium.CircleMarker([lat, lon], radius=3, color="#de2d26",
                                fill=True, popup="predicted").add_to(fmap)
        html = os.path.join(out_dir, "map.html")
        fmap.save(html)
        print(f"Wrote {png} and {html}")
    except ImportError:
        print(f"Wrote {png} (folium not installed, skipped map.html)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sample_gps.csv")
    ap.add_argument("--model", default="models/model.joblib")
    ap.add_argument("--out", default="examples")
    args = ap.parse_args()
    make_plots(args.data, args.model, args.out)


if __name__ == "__main__":
    main()
