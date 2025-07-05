# 🧭 Dementia GPS Tracker - AI-Powered Location Prediction

<div align="center">

  
  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
  [![Arduino](https://img.shields.io/badge/Arduino-Compatible-green)](https://arduino.cc)
</div>

## 🎯 Problem Statement

Dementia affects millions worldwide, with **60% of patients experiencing wandering behavior**. By combining IoT hardware with machine learning, this system predicts patient locations in advance, enabling faster caregiver response and potentially saving lives.

## 💡 Solution Overview

Our system uses real-time GPS tracking and predictive analytics to:
- 📍 Continuously monitor patient location
- 🔮 Predict future movement patterns
- 🚨 Alert caregivers before patients get lost
- 📊 Provide insights into movement behaviors

## 🧪 How to Use

```bash
# 1. Clone the repository 
git clone https://github.com/yourusername/GPS-Location-Predictor.git
cd GPS-Location-Predictor

# 2. Install required Python packages
pip install -r requirements.txt
```

## 🛠️ Steps to Run the Project
1. Upload your .csv GPS file (must follow [DATA_FORMAT.md]). 
2. Open and run `📄 Location prediction.ipynb` notebook.
   - It will handle **data preprocessing**, **model training**, and **prediction** based on your input.

## 📂 Project Structure

This repository contains all core files needed for end-to-end location prediction using GPS data:

| File / Folder                     | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `📄 Location prediction.ipynb`| All-in-one notebook that performs data preprocessing, model training, and future location prediction |
| `📄 DATA_FORMAT.md`              | Defines the required format for the input GPS `.csv` file, including column order, valid formats, and sample data |
| `📄 ARCHITECTURE.md`             | Contains system architecture diagram and component-level explanation |
| `📄 ML_Models.md`                | Details machine learning models used, tuning strategies, evaluation metrics, and reasoning |
| `📄 README.md`                   | Main project documentation with setup steps, usage guide, and future work suggestions |

> 🔗 Tip: See [`DATA_FORMAT.md`](DATA_FORMAT.md) for details on how your input GPS data should be structured before running preprocessing.

## 🏗️ System Architecture

See full system explanation and diagram in [ARCHITECTURE.md](ARCHITECTURE.md).

## 🧠 Machine Learning Models

See detailed explanation of the models used, their tuning strategies, evaluation metrics, and reasons for selection in [ML_Models.md](ML_Models.md).

## 🔮 Future Improvements

- Add a real-time alert system using GSM module or mobile app. 
- Deploy model on microcontroller to make it edge-capable (without laptop/Colab).
- Improve prediction accuracy using deep learning or sequence models (LSTM).
- Add interactive map visualization using `Folium` or `Mapbox` for path tracking.

## 🤝 Want to Help?
Fork the repo and send a pull request with any improvements!




















