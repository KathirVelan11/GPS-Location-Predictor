# 📄 Data Format Requirements for GPS Location Predictor

This document outlines the **required format** for the CSV file containing GPS data used in the Dementia GPS Tracker project.

## 📌 Required Columns

Your CSV must contain the **following six columns**, in **this exact order**:

| Column     | Description                              | Type     | Format / Example                | Notes                                                                 |
|------------|------------------------------------------|----------|----------------------------------|-----------------------------------------------------------------------|
| `Lat`      | Latitude in decimal degrees              | Float    | `9.570306`                       | `0` or empty values are treated as **invalid** and forward-filled     |
| `Lat dir`  | Latitude direction                       | String   | `N` or `S`                       | Invalid/missing values are **forward-filled**                        |
| `Long`     | Longitude in decimal degrees             | Float    | `78.106903`                      | `0` or empty values are **invalid** and forward-filled                |
| `Long dir` | Longitude direction                      | String   | `E` or `W`                       | Invalid/missing values are **forward-filled**                        |
| `Date`     | Date of GPS reading                      | String   | `30-04-2024`                     | Invalid or missing values cause the **row to be dropped**            |
| `Time`     | Time of GPS reading                      | String   | `08:29:11` (24-hour format)      | Invalid or missing values cause the **row to be dropped**            |

---

## 🛠️ Handling Missing or Invalid Data

- **Lat & Long**:  
  → `0` or empty → replaced with `NaN` → forward-filled from previous row  
- **Lat dir & Long dir**:  
  → Missing or invalid → forward-filled  
- **Date & Time**:  
  → Missing or malformed → row is **dropped** during preprocessing

The `Data Preprocessing.ipynb` notebook handles these cases automatically.

---

## 📋 Sample Data

```csv
Lat,Lat dir,Long,Long dir,Date,Time
9.570306,N,78.106903,E,30-04-2024,08:29:11
0,,0,,30-04-2024,08:29:30
9.570318,N,78.106887,E,30-04-2024,08:29:31
9.570319,N,78.106887,E,30-04-2024,08:29:32
9.570319,N,78.106887,E,30-04-2024,08:29:33
9.570319,N,78.106887,E,30-04-2024,08:29:34
0,N,0,E,30-04-2024,08:29:35
9.570319,N,78.106887,E,30-04-2024,08:29:36
9.570319,N,78.106887,E,30-04-2024,08:29:37
