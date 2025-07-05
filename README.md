# 🧭 Dementia GPS Tracker - AI-Powered Location Prediction

<div align="center">
  
  
  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
  [![Arduino](https://img.shields.io/badge/Arduino-Compatible-green)](https://arduino.cc)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  [![Contributors](https://img.shields.io/github/contributors/yourusername/dementia-gps-tracker)](https://github.com/yourusername/dementia-gps-tracker/graphs/contributors)
</div>

## 🎯 Problem Statement

Dementia affects millions worldwide, with **60% of patients experiencing wandering behavior**. This project combines IoT hardware and machine learning to predict patient locations, potentially saving lives through early intervention.

## 💡 Solution Overview

Our system uses real-time GPS tracking and predictive analytics to:
- 📍 Continuously monitor patient location
- 🔮 Predict future movement patterns
- 🚨 Alert caregivers before patients get lost
- 📊 Provide insights into movement behaviors

## 🏗️ System Architecture

```mermaid
graph TD
    A[GPS Module] --> B[Arduino + SD Card]
    B --> C[Data Collection]
    C --> D[Feature Engineering]
    D --> E[ML Model Training]
    E --> F[Location Prediction]
    F --> G[Caregiver Alert System]
