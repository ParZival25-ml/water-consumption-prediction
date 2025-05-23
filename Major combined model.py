
# RandomForestRegressor Model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df = pd.read_excel('/content/merged.xlsx')  # File destination must change according to the position

# Convert 'Day' to datetime
df['Day'] = pd.to_datetime(df['Day'])
df = df.drop(columns=["Unit(Gallon)"])

# Correlation heatmap graph
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Matrix (RF)")
plt.show()

# Sort by date
df = df.sort_values('Day')

# Define features and target
features = ['Temperature', 'Humidity', 'Season Factor', 'Holidays', 'Household_size']
target = 'Unit(Litre)'

# Train-test split (last 365 days for testing)
train_df = df.iloc[:-365]
test_df = df.iloc[-365:]

X_train = train_df[features]
y_train = train_df[target]
X_test = test_df[features]
y_test = test_df[target]

# Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation metrics
mseR = mean_squared_error(y_test, y_pred)
rmseR = np.sqrt(mseR)
r2R = r2_score(y_test, y_pred)
accuracyR = 100 * r2R

# Print results
print(f"\nModel Performance:")
print(f"Mean Squared Error (MSE): {mseR:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmseR:.2f}")
print(f"R² Score: {r2R:.4f}")
print(f"Accuracy: {accuracyR:.2f}%")

# Optional: Check for overfitting
"""train_pred = model.predict(X_train)
train_r2 = r2_score(y_train, train_pred)
print(f"\nTraining R² Score: {train_r2:.4f}")
print(f"Overfitting Gap: {train_r2 - r2:.4f}")"""

# Create a DataFrame for visualization
plot_df = pd.DataFrame({
    "Date": test_df["Day"].values,
    "Actual": y_test.values,
    "Predicted": y_pred,
})
plot_df["Residuals"] = plot_df["Actual"] - plot_df["Predicted"]

# Plotting

# 1. Line Plot - Actual vs Predicted over time
plt.figure(figsize=(10, 5))
plt.plot(plot_df["Date"], plot_df["Actual"], label="Actual", color="blue")
plt.plot(plot_df["Date"], plot_df["Predicted"], label="Predicted", color="red")
plt.title("Actual vs Predicted Over Time (RF)")
plt.xlabel("Date")
plt.ylabel("Unit(Litre)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Scatter Plot - Actual vs Predicted
plt.figure(figsize=(10, 5))
plt.scatter(plot_df["Actual"], plot_df["Predicted"], alpha=0.6, color="purple")
plt.plot([plot_df["Actual"].min(), plot_df["Actual"].max()],
         [plot_df["Actual"].min(), plot_df["Actual"].max()], 'b--')
plt.title("Actual vs Predicted Scatter (RF)")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Residuals Over Time
plt.figure(figsize=(10, 5))
plt.plot(plot_df["Date"], plot_df["Residuals"], color="orange")
plt.axhline(0, linestyle="--", color="red")
plt.title("Residuals Over Time (RF)")
plt.xlabel("Date")
plt.ylabel("Residuals")
plt.grid(True)
plt.tight_layout()
plt.show()

# Prophet Model
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("/content/merged.xlsx")
df['Day'] = pd.to_datetime(df['Day'])
df = df.drop(columns=["Unit(Gallon)"])
df = df.sort_values("Day")

# Rename for Prophet
df = df.rename(columns={"Day": "ds", "Unit(Litre)": "y"})

# Add external regressors
regressors = ['Temperature', 'Humidity', 'Season Factor', 'Holidays', 'Household_size']
df = df[['ds', 'y'] + regressors]

# Prophet model with extra regressors
model = Prophet()
for reg in regressors:
    model.add_regressor(reg)

# Train-test split: last 365 days as test
train_df = df.iloc[:-365]
test_df = df.iloc[-365:]

# Fit model
model.fit(train_df)

# Make future dataframe (365 days)
future = test_df[['ds'] + regressors]
forecast = model.predict(future)

# Evaluation
y_true = test_df['y'].values
y_pred = forecast['yhat'].values

mseP = mean_squared_error(y_true, y_pred)
rmseP = np.sqrt(mseP)
r2P = r2_score(y_true, y_pred)
accuracyP = 100 * r2P

# Print scores
print(f"\n Prophet Model Performance:")
print(f"MSE: {mseP:.2f}")
print(f"RMSE: {rmseP:.2f}")
print(f"R² Score: {r2P:.4f}")
print(f"Accuracy: {accuracyP:.2f}%")

# Create a comparison DataFrame
plot_df = pd.DataFrame({
    "Date": test_df["ds"].values,
    "Actual": test_df["y"].values,
    "Predicted": forecast["yhat"].values
})
plot_df["Residuals"] = plot_df["Actual"] - plot_df["Predicted"]

# Plot results

# 1. Line Plot: Actual vs Predicted over time
plt.figure(figsize=(10, 5))
plt.plot(test_df['ds'], y_true, label="Actual", linewidth=2)
plt.plot(test_df['ds'], y_pred, label="Predicted (Prophet)",  color="red")
plt.xlabel("Date")
plt.ylabel("Unit (Litre)")
plt.title("Actual vs Predicted Water Consumption (Prophet)")
plt.legend()
plt.tight_layout()
plt.show()

# 2. Scatter Plot: Actual vs Predicted
plt.figure(figsize=(10, 5))
plt.scatter(plot_df["Actual"], plot_df["Predicted"], alpha=0.6, color="purple")
plt.plot([plot_df["Actual"].min(), plot_df["Actual"].max()],
         [plot_df["Actual"].min(), plot_df["Actual"].max()], 'r--')
plt.title("Actual vs Predicted Scatter (Prophet)")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Residuals Over Time
plt.figure(figsize=(10, 5))
plt.plot(plot_df["Date"], plot_df["Residuals"], color="orange")
plt.axhline(0, linestyle="--", color="red")
plt.title("Residuals Over Time (Prophet)")
plt.xlabel("Date")
plt.ylabel("Residuals")
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. Heatmap of Correlations (with all features)
plt.figure(figsize=(10, 5))
heatmap_data = df[["y"] + regressors]
sns.heatmap(heatmap_data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap (Prophet)")
plt.tight_layout()
plt.show()

# SARIMA Model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Step 1: Load data
df = pd.read_excel("/content/merged.xlsx")

if 'Day' in df.columns:
    df.drop('Day', axis=1, inplace=True)
df = df.drop(columns=["Unit(Gallon)"])

# Step 2: Prepare datetime index
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
else:
    df.index = pd.date_range(start='2020-01-01', periods=len(df), freq='6H')

# Step 3: Encode categorical variables
label_enc = LabelEncoder()
if df['Season Factor'].dtype == 'object':
    df['Season Factor'] = label_enc.fit_transform(df['Season Factor'])
if df['Holidays'].dtype == 'object':
    df['Holidays'] = label_enc.fit_transform(df['Holidays'])

# Step 4: Define target and exogenous variables
y = df['Unit(Litre)']
exog = df[['Temperature', 'Humidity', 'Season Factor', 'Holidays', 'Household_size']]

# Step 5: Train/Test split (last 365 days for test)
train_y = y.iloc[:-365]
test_y = y.iloc[-365:]
train_exog = exog.iloc[:-365]
test_exog = exog.iloc[-365:]

# Step 6: Fit SARIMAX
model = SARIMAX(train_y,
                exog=train_exog,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False,
                enforce_invertibility=False)
results = model.fit()

# Step 7: Predict & Residuals
pred = results.predict(start=test_y.index[0],
                       end=test_y.index[-1],
                       exog=test_exog)
df['Residuals'] = test_y - pred

# Step 8: Evaluate
mseS = mean_squared_error(test_y, pred)
rmseS = np.sqrt(mseS)
r2S = r2_score(test_y, pred)
accuracyS = r2S * 100

print(f"MSE: {mseS:.2f}")
print(f"RMSE: {rmseS:.2f}")
print(f"R² Score: {r2S:.4f}")
print(f"Accuracy: {accuracyS:.2f}%")

# Step 9: Visualization

# 1. Actual vs Predicted (Line Plot)
plt.figure(figsize=(10, 5))
plt.plot(test_y, label='Actual')
plt.plot(pred, label='Predicted',  color="red")
plt.title('Actual vs Predicted (SARIMA)')
plt.legend()
plt.tight_layout()
plt.show()

# 2. Scatter Plot: Actual vs Predicted
plt.figure(figsize=(10, 5))
plt.scatter(test_y, pred, alpha=0.6, color="purple")
plt.plot([test_y.min(), test_y.max()],
         [test_y.min(), test_y.max()], 'r--')
plt.title("Actual vs Predicted Scatter (SARIMA)")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Residuals Over Time
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Residuals'], color="orange" )
plt.axhline(0, linestyle="--", color="red")
plt.title("Residuals Over Time (SARIMA)")
plt.tight_layout()
plt.show()

# 8. Heatmap of Correlation
plt.figure(figsize=(10, 5))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap (SARIMA)")
plt.tight_layout()
plt.show()

# Deep Neural Network (DNN) Model
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
import warnings
import seaborn as sns

# Load data
df = pd.read_excel("/content/merged.xlsx")
df['Day'] = pd.to_datetime(df['Day'])
df = df.sort_values("Day")
df = df.drop(columns=["Unit(Gallon)"])

# Features and target
features = ['Temperature', 'Humidity', 'Season Factor', 'Holidays', 'Household_size']
target = 'Unit(Litre)'

# Train-test split (365 days test)
train_df = df.iloc[:-365]
test_df = df.iloc[-365:]

X_train = train_df[features]
X_test = test_df[features]
y_train = train_df[target].values
y_test = test_df[target].values

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the DNN model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

# Train model
history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=0)

# Predict
y_pred = model.predict(X_test_scaled).flatten()

# Evaluation
mseD = mean_squared_error(y_test, y_pred)
rmseD = np.sqrt(mseD)
r2D = r2_score(y_test, y_pred)
accuracyD = 100 * r2D

print(f"\n DNN Model Performance:")
print(f"MSE: {mseD:.2f}")
print(f"RMSE: {rmseD:.2f}")
print(f"R² Score: {r2D:.4f}")
print(f"Accuracy: {accuracyD:.2f}%")

# Plot Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.plot(test_df['Day'], y_test, label='Actual', linewidth=2)
plt.plot(test_df['Day'], y_pred, label='Predicted (DNN)', linestyle='-', color='red')
plt.xlabel('Date')
plt.ylabel('Unit (Litre)')
plt.title('Actual vs Predicted Water Consumption (DNN)')
plt.legend()
plt.tight_layout()
plt.show()

# Plot training history
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Training Loss Over Epochs (DNN)')
plt.xlabel('Epoch')
plt.ylabel('MSE Loss')
plt.legend()
plt.tight_layout()
plt.show()

# Scatter Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.6, color='purple')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Scatter Plot: Actual vs Predicted (DNN)')
plt.grid(True)
plt.tight_layout()
plt.show()

residuals = y_test - y_pred

# Residuals over time
plt.figure(figsize=(10, 6))
plt.plot(residuals,color='orange')
plt.axhline(0, color='red', linestyle='--')
plt.title('Residuals Over Time (DNN)')
plt.xlabel('Days')
plt.ylabel('Residuals')
plt.grid(True)
plt.tight_layout()
plt.show()

# Heatmap of Correlation
corr = df[features + ['Unit(Litre)']].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap (DNN)")
plt.tight_layout()
plt.show()

# Graph for the comparison of accuracies of different models
# Define the evaluation metrics for each model
evaluation_data = {
    'Model': ['Random Forest', 'Prophet', 'SARIMA', 'DNN'],
    'MSE': [mseR, mseP, mseS, mseD],
    'RMSE': [rmseR, rmseP, rmseS, rmseD],
    'R2': [r2R, r2P, r2S, r2D],
    'Accuracy (%)': [accuracyR, accuracyP, accuracyS, accuracyD]
}

# Convert to DataFrame
df_eval = pd.DataFrame(evaluation_data)

# Set model names as index
df_eval.set_index('Model', inplace=True)

# Plot grouped bar charts for each metric
metrics = ['MSE', 'RMSE', 'R2', 'Accuracy (%)']
df_eval[metrics].plot(kind='bar', figsize=(12, 6), colormap='tab10')

plt.title("Model Evaluation Metrics Comparison")
plt.ylabel("Score")
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.legend(title="Metric")
plt.show()
