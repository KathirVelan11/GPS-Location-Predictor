# 🧠 Machine Learning Models for Dementia GPS Tracker

This document provides an overview of the machine learning models used in the Dementia GPS Tracker project to predict patient locations based on GPS data which includes:

- Polynomial Regression  
- Random Forest Regressor  
- XGBoost Regressor  

Each model is optimized using hyperparameter tuning methods (`RandomizedSearchCV`, `GridSearchCV`, `BayesSearchCV`) and evaluated using cross-validation techniques (`KFold`, `ShuffleSplit`).

---

## 🎯 Overview

The goal of the machine learning component is to **predict latitude and longitude coordinates** (and their directional indicators) using temporal features from GPS data such as:

- Date  
- Time  
- Derived features (e.g., day of the week, time of day, etc.)

These models are trained on preprocessed data (see [`DATA_FORMAT.md`](DATA_FORMAT.md)) and evaluated using metrics like:

- Mean Squared Error (MSE)  
- Mean Absolute Error (MAE)  
- Root Mean Squared Error (RMSE)  
- R-squared (R²)  
- Adjusted R-squared  

---

## 🔍 Models Used

### 1. 📈 Polynomial Regression

#### ✅ Description
Polynomial Regression models **non-linear relationships** by transforming input features into polynomial terms and applying linear regression to them.

#### ⚙️ Implementation
- **Pipeline**: Combines `PolynomialFeatures` and `LinearRegression`  
- **Features**: Uses processed features such as `Days_from_ref`, `Seconds_from_midnight`, `HourDayInteraction`, `Time_sin`, `Time_cos`, etc.

#### 🔧 Hyperparameters
- `polynomial_features__degree` (e.g., 2, 3, 4)  
- `polynomial_features__interaction_only` (True/False)  
- `polynomial_features__include_bias` (True/False)

#### 🔍 Tuning Methods
- `RandomizedSearchCV`  
- `GridSearchCV`  
- `BayesSearchCV`

#### 🔁 Cross-Validation
- `KFold` (5 splits)  
- `ShuffleSplit` (5 splits, 20% test size)

#### 📊 Evaluation
- MSE, MAE, RMSE, R², Adjusted R²  
- Predicted vs. actual scatter plots

#### 💡 Why Use It?
Useful for modeling **cyclical behaviors** in patient movement (e.g., daily routines). Overfitting is mitigated via tuning and cross-validation.

---

### 2. 🌲 Random Forest Regressor

#### ✅ Description
Random Forest builds multiple decision trees and averages their predictions. It’s **robust**, **non-linear**, and handles **feature interactions** well.

#### ⚙️ Implementation
- `RandomForestRegressor` (from scikit-learn, with `random_state=42`)  
- Uses same features as Polynomial Regression

#### 🔧 Hyperparameters
- `n_estimators`: Number of trees  
- Additional parameters explored during tuning

#### 🔍 Tuning Methods
- `RandomizedSearchCV`  
- `GridSearchCV`  
- `BayesSearchCV`

#### 🔁 Cross-Validation
- `KFold` (5 folds)  
- `ShuffleSplit` (5 splits, 20% test size)

#### 📊 Evaluation
- MSE, MAE, RMSE, R², Adjusted R²  
- Feature importance visualizations  
- Predicted vs. actual scatter plots

#### 💡 Why Use It?
Good at handling **noisy GPS data**, capturing **complex patterns**, and preventing overfitting.

---

### 3. ⚡ XGBoost Regressor

#### ✅ Description
`XGBoostRegressor` builds decision trees iteratively using **gradient boosting** to optimize performance. Known for **speed**, **accuracy**, and **regularization**.

#### ⚙️ Implementation
- `XGBRegressor` from the XGBoost library (with `random_state=42`)  
- Uses same preprocessed features as other models

#### 🔧 Hyperparameters
- `n_estimators`: e.g., 50, 100, 150  
- `max_depth`: e.g., 3, 6, 9  
- `learning_rate`: e.g., 0.01, 0.1, 0.2  
- `subsample`, `colsample_bytree`, `gamma`, `reg_lambda`, `reg_alpha`

#### 🔍 Tuning Methods
- `RandomizedSearchCV`  
- `GridSearchCV`  
- `BayesSearchCV`

#### 🔁 Cross-Validation
- `KFold` (5 folds)  
- `ShuffleSplit` (5 splits, 20% test size)

#### 📊 Evaluation
- MSE, MAE, RMSE, R², Adjusted R²  
- Feature importance plots  
- Scatter plots of predicted vs. actual coordinates

#### 💡 Why Use It?
Highly accurate, less prone to overfitting, handles **non-linear relationships**, and performs well on real-world, sparse, or noisy data.

---

## 🔍 Hyperparameter Tuning & Cross-Validation

### 🎯 Tuning Methods

- **RandomizedSearchCV**: Fast, good for large search spaces  
- **GridSearchCV**: Exhaustive and thorough  
- **BayesSearchCV**: Bayesian optimization for intelligent exploration

### 🔁 Cross-Validation Techniques

- **KFold**:
  - 5-fold split
  - Ensures every data point is validated
- **ShuffleSplit**:
  - 5 randomized splits
  - Faster on large datasets

---

## 📏 Model Evaluation Metrics

| Metric       | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| MSE          | Mean of squared errors between predicted and true values                   |
| MAE          | Mean of absolute errors, less sensitive to outliers                        |
| RMSE         | Square root of MSE, gives error in same units as output                    |
| R²           | Proportion of variance explained by model (closer to 1 is better)          |
| Adjusted R² | Adjusts R² for the number of predictors to penalize overly complex models   |

**Visualizations:**
- Predicted vs. actual scatter plots
- Feature importance (Random Forest, XGBoost)

---

## ✅ Model Selection & Deployment

- The best model is chosen based on **lowest MSE** or **highest R²** on the **test set**.
- Saved to disk (e.g., `best_rf_model.pkl`)
- Used in `New Prediction.py` for real-time predictions

---

## 🧩 Why These Models?

| Model               | Strengths                                                                 |
|--------------------|---------------------------------------------------------------------------|
| Polynomial Regression | Captures non-linear patterns, useful for daily behavior cycles          |
| Random Forest         | Robust to noise, handles feature interactions                          |
| XGBoost               | High performance, regularized, less overfitting, ideal for real-time    |

---

## 🔗 Usage in the Project

- **Training**: Performed in `Model Training.ipynb` using processed data from `Data Preprocessing.ipynb`
- **Prediction**: Performed in `New Prediction.py` using best saved model
- **Integration**: Coordinates predicted are used to **trigger caregiver alerts**, preventing patient wandering

---
