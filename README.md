📊 Water Consumption Prediction Project: 
The primary target of this project is to create a machine learning based model to forecast water consumption 
with high accuracy. By analyzing daily water consumption data and different factors like temperature, 
humidity, season factor, holidays, and number of people in a house, project aims to: 

• Provide accurate water consumption predictions. 

• Examine many models to determine their accuracy. 

• Provide clear insights for effective resource planning and informed policymaking. 

• Consider sustainable water resource management by reducing wastage and optimizing allocation.

This project is motivated by growing demand of water resources which is due to rapid increase of urbanization and population. Since water is a limited resource, this project shows how important precise forecasting is, which will promote the effective use of water. Additionally, it also aims to establish long-term capacities that will help in future planning for water infrastructures and in management of resources as well as to provide well-organized plan to minimize resource allocation to prevent major shortages.

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

Compare model performance using MSE, RMSE and R² Score.

Visualize predictions, residuals, and feature correlations


📷 Visualizations

Each model includes:

- Actual vs Predicted Line Plots

- Scatter Plots

- Residual Analysis

- Correlation Heatmaps

📂 Structure

The entire implementation is contained in a single Python file: `Major combined model.py`.

⚠️ **Note**: The file reads from `merged.xlsx`. You must ensure this Excel file is available in your working directory or update the path in the script accordingly.

The models are trained and tested on a dataset containing:

- 📅 Date (`Day`)
- 🌡️ Temperature
- 💧 Humidity
- 🏖️ Season Factor
- 📅 Holidays
- 👨‍👩‍👧 Household Size
- 💦 Water consumption (`Unit(Litre)`)

The target variable - `Unit(Litre)`

