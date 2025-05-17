📊 Combined Model Project: Water Consumption Forecasting
This project presents a comparative analysis of multiple machine learning and time series forecasting models for predicting water consumption in litres. The models included are:

✅ Random Forest Regressor
🔮 Facebook Prophet
📈 SARIMA (Seasonal ARIMA)
🧠 Deep Neural Network (DNN)

🧪 Dataset
The dataset used for this project is included as `merged.xlsx`.  
It contains water consumption data along with environmental and temporal features:

- Date (Day)
- Temperature
- Humidity
- Season Factor
- Holidays
- Household Size
- Water Consumption (Unit in Litres)

This project includes two datasets in the `data/` folder:

- `DATASET.xlsx`: The raw dataset before any cleaning or transformation.
- `merged.xlsx`: The processed and cleaned dataset used for training and evaluating all models.

Ensure paths in the code (e.g., `pd.read_excel()`) match the location of these files (`data/merged.xlsx`).

📌 Objectives
Build and evaluate different forecasting models

Compare model performance using MSE, RMSE, R² Score, and Accuracy

Visualize predictions, residuals, and feature correlations

📷 Visualizations
Each model includes:

Actual vs Predicted Line Plots
Scatter Plots
Residual Analysis
Correlation Heatmaps

📂 Structure
The entire implementation is contained in a single Python file: Major combined model.py.

⚠️ **Note**: The file reads from `merged.xlsx`. You must ensure this Excel file is available in your working directory or update the path in the script accordingly.

The models are trained and tested on a dataset containing:

- 📅 Date (`Day`)
- 🌡️ Temperature
- 💧 Humidity
- 🏖️ Season Factor
- 📅 Holidays
- 👨‍👩‍👧 Household Size
- 💦 Water consumption (`Unit(Litre)`)

The target variable - "Unit(Litre)"

