# 🧭 Dementia Patient Location Tracking

<div align="center">

  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
  [![Arduino](https://img.shields.io/badge/Arduino-Compatible-green)](https://arduino.cc)
  [![Best Model R²](https://img.shields.io/badge/Random%20Forest%20R²-0.99999-brightgreen)](#-results)
</div>

An end-to-end system that logs a dementia patient's GPS trail with an Arduino and
**predicts their location from date & time** using machine learning — so caregivers
can respond before a patient wanders off.

## 🎯 Problem Statement

Dementia affects millions worldwide, with **~60% of patients experiencing wandering behavior**. By combining IoT hardware with machine learning, this system predicts patient locations in advance, enabling faster caregiver response and potentially saving lives.

## 💡 Solution Overview

- 📍 Continuously log patient location (Arduino + GPS + SD card)
- 🔮 Predict future coordinates from temporal features (date/time)
- 🚨 Alert caregivers before patients get lost
- 📊 Provide insights into movement behaviors

## 📊 Results

Trained on **4,791 real GPS readings** (features shape `(4791, 18)`, targets `(4791, 6)`).
Three models were tuned and compared; **Random Forest** was selected as the best.

| Model                 | Test R² Score | Notes                                  |
|-----------------------|:-------------:|----------------------------------------|
| 🌲 **Random Forest**  | **0.99999**   | ✅ Best model — near-perfect fit        |
| 📈 Polynomial Regression | 0.9977     | Captures daily cyclical routines        |
| ⚡ XGBoost (base)      | 0.333         | Baseline before extensive tuning        |

### 🔮 Example Prediction

Given a date & time, the notebook predicts the patient's coordinates:

```
Input   →  Date: 20/05/2024   Time: 15:51:00
Output  →  Predicted Latitude : 9.5703399709
           Predicted Longitude: 78.1067810017
```

> 📍 These coordinates fall in the Tamil Nadu region (~9.57°N, 78.10°E), matching the training area.

## 🧪 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/KathirVelan11/GPS-Location-Predictor.git
cd GPS-Location-Predictor

# 2. Install required Python packages
pip install -r requirements.txt
```

### Steps to Run
1. Prepare a `.csv` GPS file that follows [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md).
2. Open and run **`Location prediction.ipynb`** — it handles **preprocessing**, **model training**, and **prediction** in one place.
3. At the final step, enter a date and time to get the predicted location.

## 📂 Project Structure

```
GPS-Location-Predictor/
├── Location prediction.ipynb    # All-in-one: preprocessing → training → prediction
├── requirements.txt             # Python dependencies
├── Hardware/
│   └── GPS_data_logging.ino     # Arduino GPS → SD-card CSV logger
├── docs/
│   ├── DATA_FORMAT.md           # Required CSV format & sample data
│   ├── ML_MODELS.md             # Models, tuning, metrics & rationale
│   └── ARCHITECTURE.md          # System architecture diagram
└── README.md
```

## 📟 Arduino GPS Logger

The hardware module collects real-time GPS coordinates and logs them to a `.csv` file on an SD card, ready for the prediction pipeline.

**Components:** 🛰️ Neo 6M GPS Module · 💡 Arduino Uno · 💾 SD Card + Module · 🔌 Jumper Wires · 🔋 Power Bank

`Hardware/GPS_data_logging.ino` reads GPS data over SoftwareSerial, extracts latitude, longitude and IST-adjusted date/time, and writes each record to `data.csv`.

> ✅ The generated `.csv` already follows [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md) — upload it directly into the Python pipeline.

## 🏗️ System Architecture

See the full diagram and explanation in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🧠 Machine Learning Models

See detailed model descriptions, tuning strategies and evaluation metrics in [docs/ML_MODELS.md](docs/ML_MODELS.md).

## 🔮 Future Improvements

- Real-time alerts via GSM module or mobile app
- Deploy on microcontroller for edge inference (no laptop/Colab)
- Sequence models (LSTM) for higher accuracy
- Interactive map visualization with `Folium` or `Mapbox`

## 🤝 Contributing

Fork the repo and send a pull request with any improvements!
