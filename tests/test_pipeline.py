"""Unit tests for the GPS location predictor pipeline."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from generate_sample_data import generate  # noqa: E402
from metrics import distance_report, haversine_m  # noqa: E402
from preprocessing import (  # noqa: E402
    FEATURE_COLUMNS,
    build_features,
    load_dataset,
)


def test_haversine_zero_distance():
    assert haversine_m(9.57, 78.10, 9.57, 78.10) == 0.0


def test_haversine_known_distance():
    # ~1 degree of latitude is about 111 km.
    d = haversine_m(0.0, 0.0, 1.0, 0.0)
    assert 110_000 < d < 112_000


def test_distance_report_keys():
    true = np.array([[9.57, 78.10], [9.58, 78.11]])
    pred = np.array([[9.57, 78.10], [9.58, 78.11]])
    rep = distance_report(true, pred)
    assert rep["mean_error_m"] == 0.0
    assert rep["n_samples"] == 2
    assert set(rep) >= {"mean_error_m", "median_error_m", "p90_error_m"}


def test_build_features_no_nans_or_infs():
    # Regression test for the notebook's log1p-on-sin/cos bug.
    df = generate(days=3)
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], dayfirst=True)
    df = df.rename(columns={"Lat ": "lat", "Long ": "lon"})
    feats = build_features(df)[FEATURE_COLUMNS].values
    assert np.isfinite(feats).all()


def test_load_dataset_roundtrip(tmp_path):
    csv = tmp_path / "sample.csv"
    generate(days=5).to_csv(csv, index=False)
    df = load_dataset(str(csv))
    assert len(df) > 0
    for col in FEATURE_COLUMNS + ["lat", "lon", "datetime"]:
        assert col in df.columns
    # Rows must be chronologically ordered for the time-based split.
    assert df["datetime"].is_monotonic_increasing
