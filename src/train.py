"""Train the location predictor with an honest, leakage-free evaluation.

Why a time-based split (and not ``train_test_split(random_state=...)``):
GPS log rows are sampled minutes apart, so consecutive rows are almost
identical. A *random* split scatters near-duplicate neighbours across train and
test, letting the model "memorise" the test points -- that is exactly what
produced the suspicious R2 ~ 0.99999 in the original notebook. Splitting on
time (train on the earlier days, test on the later days) measures what we
actually want: can the model predict *future* locations it has never seen.

Usage:
    python src/train.py --data data/sample_gps.csv --out models/
"""
from __future__ import annotations

import argparse
import json
import os

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

from metrics import distance_report
from preprocessing import FEATURE_COLUMNS, TARGET_COLUMNS, load_dataset


def time_split(df, test_frac=0.2):
    """Split chronologically: earliest (1-test_frac) train, latest test."""
    df = df.sort_values("datetime").reset_index(drop=True)
    cut = int(len(df) * (1 - test_frac))
    return df.iloc[:cut].copy(), df.iloc[cut:].copy()


def train(data_path: str, out_dir: str):
    df = load_dataset(data_path)
    train_df, test_df = time_split(df)

    X_tr = train_df[FEATURE_COLUMNS].values
    y_tr = train_df[TARGET_COLUMNS].values
    X_te = test_df[FEATURE_COLUMNS].values
    y_te = test_df[TARGET_COLUMNS].values

    model = RandomForestRegressor(
        n_estimators=300, max_depth=12, min_samples_leaf=3,
        random_state=1, n_jobs=-1,
    )
    model.fit(X_tr, y_tr)

    pred = model.predict(X_te)
    report = distance_report(y_te, pred)

    # A naive baseline: always predict the mean training location. If the model
    # cannot beat this, it has learned nothing useful.
    baseline_pred = np.tile(y_tr.mean(axis=0), (len(y_te), 1))
    baseline = distance_report(y_te, baseline_pred)

    os.makedirs(out_dir, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURE_COLUMNS}, os.path.join(out_dir, "model.joblib"))

    results = {
        "n_train": len(train_df),
        "n_test": len(test_df),
        "split": "time-based (earliest 80% train / latest 20% test)",
        "model": {"type": "RandomForestRegressor", "n_estimators": 300, "max_depth": 12},
        "test_error": report,
        "mean_baseline_error": baseline,
        "improvement_vs_baseline_pct": round(
            100 * (1 - report["median_error_m"] / baseline["median_error_m"]), 1
        ),
    }
    with open(os.path.join(out_dir, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sample_gps.csv")
    ap.add_argument("--out", default="models")
    args = ap.parse_args()
    train(args.data, args.out)


if __name__ == "__main__":
    main()
