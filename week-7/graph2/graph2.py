import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# Load the uploaded CSV file
file_path = "sensor_data.csv"  

try:
    data = pd.read_csv(file_path)
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()

# Display the first few rows
print(data.head())

# Standardize column names
data.columns = data.columns.str.strip().str.lower()
data.rename(columns={"temperature (c)": "temperature", "humidity (%)": "humidity"}, inplace=True)

# Check if required columns exist
required_columns = {'temperature', 'humidity'}
if not required_columns.issubset(data.columns):
    print(f"Error: CSV file must contain {required_columns} columns.")
    print("Found columns:", data.columns)
    exit()

# Reshape the data for sklearn
X = data['temperature'].values.reshape(-1, 1)
Y = data['humidity'].values.reshape(-1, 1)

# Create and train the Linear Regression model
model = LinearRegression()
model.fit(X, Y)

# Print the coefficients
print(f"Intercept: {model.intercept_[0]:.2f}")
print(f"Coefficient: {model.coef_[0][0]:.2f}")

# Generate temperature range for prediction
min_temp, max_temp = X.min(), X.max()
test_temps = np.linspace(min_temp, max_temp, 100).reshape(-1, 1)

# Predict humidity for the test temperatures
predicted_humidity = model.predict(test_temps)

# Create the plot
fig = go.Figure()

# Scatter plot of original data
fig.add_trace(go.Scatter(
    x=data['temperature'], 
    y=data['humidity'], 
    mode='markers',
    name='Original Data',
    marker=dict(color='blue', size=6, opacity=0.7)
))

# Trend line from interpolated values
fig.add_trace(go.Scatter(
    x=test_temps.flatten(),
    y=predicted_humidity.flatten(),
    mode='lines',
    name='Trend Line',
    line=dict(color='red', width=2)
))

# Labels and title
fig.update_layout(
    title='Temperature vs Humidity with Trend Line',
    xaxis_title='Temperature (\u00b0C)',
    yaxis_title='Humidity (%)',
    template='plotly_white',
    margin=dict(l=40, r=40, t=40, b=40)
)

fig.show()
