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
data.rename(columns={"temperature": "temperature", "humidity": "humidity"}, inplace=True)

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
    name='Measured Data',
    marker=dict(color='deepskyblue', size=8, opacity=0.8)
))

# Trend line from interpolated values
fig.add_trace(go.Scatter(
    x=test_temps.flatten(),
    y=predicted_humidity.flatten(),
    mode='lines',
    name='Linear Regression',
    line=dict(color='darkorange', width=3)
))

# Labels and title
fig.update_layout(
    title='Linear Regression: Temperature vs Humidity',
    xaxis_title='Temperature (°C)',
    yaxis_title='Humidity (%)',
    template='plotly_dark',
    margin=dict(l=50, r=50, t=50, b=50),
    font=dict(size=14)
)

# Add annotations
fig.add_annotation(
    x=min_temp, y=model.predict([[min_temp]])[0][0],
    text=f"y = {model.intercept_[0]:.2f} + {model.coef_[0][0]:.2f}x",
    showarrow=False,
    font=dict(size=12, color='white')
)

fig.show()
