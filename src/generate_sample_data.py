"""Generate a synthetic GPS log that mimics the structure of the real
(private) dementia-patient dataset.

The real patient data cannot be shared for privacy reasons, so this script
produces a realistic stand-in: a patient with a daily routine who moves
between a few locations around Madurai, Tamil Nadu (~9.57N, 78.10E). The
output CSV matches the exact column layout the pipeline expects, so the
whole project is runnable end-to-end without the private data.

Usage:
    python src/generate_sample_data.py --out data/sample_gps.csv --days 45
"""
import argparse
import numpy as np
import pandas as pd

# A few real-world places the patient visits, with a rough daily schedule.
# (name, lat, lon, hour_start, hour_end)
PLACES = [
    ("home",    9.570300, 78.106900,  0,  8),   # night / early morning at home
    ("park",    9.572100, 78.108400,  8, 11),   # morning walk
    ("market",  9.568500, 78.104200, 11, 14),   # midday errands
    ("home",    9.570300, 78.106900, 14, 18),   # afternoon rest
    ("temple",  9.573600, 78.109900, 18, 20),   # evening visit
    ("home",    9.570300, 78.106900, 20, 24),   # night at home
]


def place_for_hour(hour: int):
    for name, lat, lon, h0, h1 in PLACES:
        if h0 <= hour < h1:
            return lat, lon
    return PLACES[0][1], PLACES[0][2]


def generate(days: int, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2024-04-30 00:00:00")
    rows = []
    ts = start
    end = start + pd.Timedelta(days=days)
    while ts < end:
        base_lat, base_lon = place_for_hour(ts.hour)
        # GPS jitter (~5-10 m) plus a little wandering while at a place.
        lat = base_lat + rng.normal(0, 0.00008)
        lon = base_lon + rng.normal(0, 0.00008)
        rows.append({
            "Lat ": round(lat, 6),
            "Lat dir": "N",
            "Long ": round(lon, 6),
            "Long dir": "E",
            "Date": ts.strftime("%d-%m-%Y"),
            "Time": ts.strftime("%H:%M:%S"),
        })
        # Sample every few minutes, like a real low-power logger.
        ts += pd.Timedelta(minutes=int(rng.integers(3, 12)))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(description="Generate synthetic GPS sample data.")
    ap.add_argument("--out", default="data/sample_gps.csv")
    ap.add_argument("--days", type=int, default=45)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    df = generate(args.days, args.seed)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
