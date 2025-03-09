import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv("gyro_data.csv")

# Remove any NaN values
df.dropna(inplace=True)

# Convert timestamp to seconds for better visualization
df["timestamp"] = (df["timestamp"] - df["timestamp"].min()) / 1000  # Convert ms to seconds

# Create subplots for distinct graphs
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# X-axis graph
axs[0].plot(df["timestamp"], df["x"], color="red", label="X-axis")
axs[0].set_ylabel("X-Axis Gyroscope (dps)")
axs[0].set_title("Gyroscope X-Axis Data Over Time")
axs[0].legend()
axs[0].grid()

# Y-axis graph
axs[1].plot(df["timestamp"], df["y"], color="green", label="Y-axis")
axs[1].set_ylabel("Y-Axis Gyroscope (dps)")
axs[1].set_title("Gyroscope Y-Axis Data Over Time")
axs[1].legend()
axs[1].grid()

# Z-axis graph
axs[2].plot(df["timestamp"], df["z"], color="blue", label="Z-axis")
axs[2].set_xlabel("Time (seconds)")
axs[2].set_ylabel("Z-Axis Gyroscope (dps)")
axs[2].set_title("Gyroscope Z-Axis Data Over Time")
axs[2].legend()
axs[2].grid()

# Adjust layout
plt.tight_layout()
plt.show()

# Create a combined graph
plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["x"], label="X-axis", color="red")
plt.plot(df["timestamp"], df["y"], label="Y-axis", color="green")
plt.plot(df["timestamp"], df["z"], label="Z-axis", color="blue")
plt.xlabel("Time (seconds)")
plt.ylabel("Gyroscope Values (dps)")
plt.title("Combined Gyroscope Data Over Time")
plt.legend()
plt.grid()
plt.show()
