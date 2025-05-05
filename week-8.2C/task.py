import sys
import time
import traceback
import os
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from arduino_iot_cloud import ArduinoCloudClient
import collections  # <-- NEW

# Arduino Credentials
DEVICE_ID = "ad32580c-c517-4b9f-992b-a0d97513d28c"
SECRET_KEY = "U0wz4F3z4CTQ5SRoruqQJH0ua"

# Variables
BUFFER_SIZE = 100  # <-- You can adjust the buffer size
cur_data = collections.deque(maxlen=BUFFER_SIZE)  # <-- Use deque as a buffer
temp_data = []
x, y, z = None, None, None

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0)  # Every 10 seconds
])

@app.callback(
    Output('live-update-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n_intervals):
    global cur_data
    if not cur_data:
        return go.Figure()

    df = pd.DataFrame(list(cur_data), columns=['Index', 'Timestamp', 'X', 'Y', 'Z'])

    fig = px.line(df, x='Timestamp', y=['X', 'Y', 'Z'], title="Live Accelerometer Data")
    fig.update_layout(xaxis_title='Time', yaxis_title='Value', legend_title='Axis')
    return fig

# Arduino Cloud Callbacks
def on_accelerometer_x_changed(client, value):
    global x
    x = value

def on_accelerometer_y_changed(client, value):
    global y
    y = value

def on_accelerometer_z_changed(client, value):
    global z
    z = value

# Main data collection loop
def start_collection():
    global cur_data, temp_data, x, y, z
    try:
        client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode=True)
        
        client.register("py_x", value=None, on_write=on_accelerometer_x_changed)
        client.register("py_y", value=None, on_write=on_accelerometer_y_changed)
        client.register("py_z", value=None, on_write=on_accelerometer_z_changed)
        
        client.start()
        last_save_time = time.time()

        index = 0

        while True:
            if x is not None and y is not None and z is not None:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                index += 1
                temp_data.append([index, timestamp, x, y, z])
                x, y, z = None, None, None

            # Every 10 seconds, update cur_data
            if time.time() - last_save_time >= 10:
                if temp_data:
                    for record in temp_data:
                        cur_data.append(record)  # <-- append one by one to the deque buffer
                    temp_data.clear()
                    last_save_time = time.time()

            client.update()

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()

if __name__ == "__main__":
    import threading

    # Start Arduino data collection in separate thread
    data_thread = threading.Thread(target=start_collection)
    data_thread.start()

    # Run Dash app
    app.run(debug=True)
