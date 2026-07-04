"""Geospatial error metrics.

For a location predictor, R2 on raw lat/lon is a poor headline number -- it is
dominated by how spread out the points are and is easy to inflate with leakage.
The metric a caregiver actually cares about is *how many metres off* the
prediction is, so we report Haversine great-circle distance.
"""
from __future__ import annotations

import numpy as np

EARTH_RADIUS_M = 6_371_000.0


def haversine_m(lat1, lon1, lat2, lon2):
    """Great-circle distance in metres between two coordinate arrays."""
    lat1, lon1, lat2, lon2 = map(np.asarray, (lat1, lon1, lat2, lon2))
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlambda / 2) ** 2
    return 2 * EARTH_RADIUS_M * np.arcsin(np.sqrt(a))


def distance_report(true_latlon, pred_latlon) -> dict:
    """Summary error stats (metres) for predicted vs. true coordinates."""
    d = haversine_m(
        true_latlon[:, 0], true_latlon[:, 1],
        pred_latlon[:, 0], pred_latlon[:, 1],
    )
    return {
        "mean_error_m": float(np.mean(d)),
        "median_error_m": float(np.median(d)),
        "p90_error_m": float(np.percentile(d, 90)),
        "max_error_m": float(np.max(d)),
        "n_samples": int(len(d)),
    }
