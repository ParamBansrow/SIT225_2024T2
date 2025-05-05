import sys  
import time  
import traceback  
import os  
import csv  
import pandas as pd  
import plotly.graph_objs as go  
from dash import Dash, dcc, html 
from dash.dependencies import Output, Input  
from arduino_iot_cloud import ArduinoCloudClient  
from threading import Thread  
from datetime import datetime  
import cv2  



DEVICE_ID = "ad32580c-c517-4b9f-992b-a0d97513d28c"  
SECRET_KEY = "U0wz4F3z4CTQ5SRoruqQJH0ua"  


cur_data = []  
csv_file = "accelerometer_data.csv"  


x, y, z = 0, 0, 0

SNAPSHOT_INTERVAL = 10  
_last_snapshot = time.time()  


MAX_RUNTIME = 1800  


cap = cv2.VideoCapture(0)  

#
if not cap.isOpened():
    print("Error: Could not open webcam. Check camera permissions in System Settings.")
    sys.exit(1)


def on_accelerometer_x_changed(client, value):
    global x
    x = value

def on_accelerometer_y_changed(client, value):
    global y
    y = value

def on_accelerometer_z_changed(client, value):
    global z
    z = value


def start_data_stream():
    global cur_data, x, y, z, _last_snapshot, cap
    start_time = time.time()

    try:
        client = ArduinoCloudClient(
            device_id=DEVICE_ID,
            username=DEVICE_ID,
            password=SECRET_KEY,
            sync_mode=True
        )

        client.register("py_x", value=None, on_write=on_accelerometer_x_changed)
        client.register("py_y", value=None, on_write=on_accelerometer_y_changed)
        client.register("py_z", value=None, on_write=on_accelerometer_z_changed)

        client.start()

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if os.stat(csv_file).st_size == 0:
                writer.writerow(['Timestamp', 'X', 'Y', 'Z'])

        while True:
            if time.time() - start_time > MAX_RUNTIME:
                print("Max runtime reached. Stopping program.")
                break

            if x is not None and y is not None and z is not None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                data_point = [timestamp, x, y, z]

                cur_data.append(data_point)
                if len(cur_data) > 50:
                    cur_data.pop(0)

                with open(csv_file, mode='a', newline='') as file:
                    csv.writer(file).writerow(data_point)

                print(data_point)
                x, y, z = None, None, None

            now = time.time()
            if now - _last_snapshot >= SNAPSHOT_INTERVAL:
                try:
                    cap.grab()
                    ret, frame = cap.retrieve()
                    if ret and frame is not None:
                        ts = datetime.now().strftime('%Y%m%dT%H%M%S')
                        img_name = f"seq_{ts}.jpg"
                        cv2.imwrite(img_name, frame)
                        print(f"Snapshot saved: {img_name}")
                    else:
                        print("Error: frame capture failed.")
                except Exception as e:
                    print(f"Exception during snapshot: {e}")

                _last_snapshot = now

            client.update()

    except Exception:
        print("Error in data stream:")
        traceback.print_exc()



def smooth_data(df, window_size=5):
    df_smoothed = df.copy()
    for col in ['X', 'Y', 'Z']:
        df_smoothed[col] = df[col].rolling(window=window_size, min_periods=1).mean()
    return df_smoothed


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Live Accelerometer Data (Last 10 Seconds)"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
])

@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    if not cur_data:
        return go.Figure()

    df = pd.DataFrame(cur_data, columns=['Timestamp', 'X', 'Y', 'Z'])
    df = smooth_data(df, window_size=5)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['X'], mode='lines+markers', name='X'))
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Y'], mode='lines+markers', name='Y'))
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Z'], mode='lines+markers', name='Z'))

    fig.update_layout(
        xaxis_title='Timestamp',
        yaxis_title='Acceleration',
        margin=dict(l=40, r=20, t=40, b=40),
        height=600
    )
    return fig



if __name__ == "__main__":
    data_thread = Thread(target=start_data_stream, daemon=True)
    data_thread.start()

    app.run(debug=False, use_reloader=False, port=8054)
    cap.release()