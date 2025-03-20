import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the CSV file
data = pd.read_csv("gyro_data.csv")  
total_samples = len(data)

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Gyroscope Data Visualization", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Graph Type:"),
        dcc.Dropdown(
            id="graph-type",
            options=[
                {"label": "Scatter Plot", "value": "scatter"},
                {"label": "Line Chart", "value": "line"},
                {"label": "Distribution Plot", "value": "dist"}
            ],
            value="scatter"
        ),
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    html.Div([
        html.Label("Select Variables:"),
        dcc.Dropdown(
            id="variables",
            options=[
                {"label": col, "value": col} for col in data.columns
            ],
            value=["x", "y", "z"],
            multi=True
        ),
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    html.Div([
        html.Label("Number of Samples to Display:"),
        dcc.Input(id="num-samples", type="number", value=100, min=1, max=total_samples, step=1)
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    html.Div([
        html.Button("Previous", id="prev-button", n_clicks=0),
        html.Button("Next", id="next-button", n_clicks=0),
    ], style={"textAlign": "center", "padding": "10px"}),

    dcc.Graph(id="graph"),
    html.Div(id="summary-table")
])

# Callback to update the graph and summary table
@app.callback(
    [Output("graph", "figure"), Output("summary-table", "children")],
    [Input("graph-type", "value"), Input("variables", "value"),
     Input("num-samples", "value"), Input("prev-button", "n_clicks"),
     Input("next-button", "n_clicks")]
)
def update_graph(graph_type, variables, num_samples, prev_clicks, next_clicks):
    # Calculate start and end indices for slicing
    start_idx = (prev_clicks - next_clicks) * num_samples
    start_idx = max(0, min(start_idx, total_samples - num_samples))
    end_idx = start_idx + num_samples

    # Filter the data for the selected range
    filtered_data = data.iloc[start_idx:end_idx]
    filtered_data['index'] = range(start_idx, end_idx)  # Add an index column for the x-axis

    # Create the graph based on the selected graph type
    if graph_type == "scatter":
        fig = px.scatter(
            filtered_data.melt(id_vars='index', value_vars=variables),
            x="index", y="value", color="variable", title="Scatter Plot"
        )
    elif graph_type == "line":
        fig = px.line(
            filtered_data.melt(id_vars='index', value_vars=variables),
            x="index", y="value", color="variable", title="Line Chart"
        )
    elif graph_type == "dist":
        fig = px.histogram(
            filtered_data.melt(value_vars=variables),
            x="value", color="variable", title="Distribution Plot", barmode="overlay"
        )

    # Create a summary table
    summary = filtered_data[variables].describe().reset_index()
    summary_table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in summary.columns])),
        html.Tbody([
            html.Tr([html.Td(summary.iloc[i][col]) for col in summary.columns])
            for i in range(len(summary))
        ])
    ])

    return fig, summary_table


# Run the app
if __name__ == "_main_":
    app.run_server(debug=True)