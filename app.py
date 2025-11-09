import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import time

# ------------------------------------------------------------
# App setup
# ------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Gunicorn looks for this

# ------------------------------------------------------------
# Dummy data for charts
# ------------------------------------------------------------
df = pd.DataFrame({
    "Category": ["Apples", "Bananas", "Cherries", "Dates"],
    "Value": [40, 25, 30, 10]
})

# ------------------------------------------------------------
# Layout
# ------------------------------------------------------------
app.layout = dbc.Container([
    # Logo + Header
    dbc.Row([
        dbc.Col(html.Img(src="https://upload.wikimedia.org/wikipedia/en/7/7b/Texas_A%26M_University_logo.svg",
                         style={"height": "70px"}), width="auto"),
        dbc.Col(html.H2("Mai Shan Yun Dashboard", className="text-center my-auto"),
                width=True)
    ], align="center", className="mb-4"),

    html.Hr(),

    # Dropdown for chart selection
    dbc.Row([
        dbc.Col([
            html.Label("Select a chart:", className="fw-bold"),
            dcc.Dropdown(
                id="chart-dropdown",
                options=[
                    {"label": "Sales Overview", "value": "sales"},
                    {"label": "Revenue Breakdown", "value": "revenue"},
                    {"label": "Forecasting", "value": "forecast"}
                ],
                value="sales",
                clearable=False,
            )
        ], width=4)
    ]),

    html.Br(),

    # Loading spinner with A&M quote
    dcc.Loading(
        id="loading-spinner",
        type="circle",
        fullscreen=False,
        children=html.Div(id="chart-container"),
        style={"marginTop": "40px"}
    ),

    html.Div(id="quote", className="text-center mt-4 fst-italic text-secondary")
], fluid=True)

# ------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------
@app.callback(
    Output("chart-container", "children"),
    Output("quote", "children"),
    Input("chart-dropdown", "value")
)
def update_chart(selected_chart):
    # Simulate load time for demo
    time.sleep(2)

    # Example quotes to rotate
    quotes = {
        "sales": "“The Aggie Spirit never quits.”",
        "revenue": "“From the outside looking in, you can’t understand it. From the inside looking out, you can’t explain it.”",
        "forecast": "“Leadership and loyalty — the Aggie way.”"
    }

    # Create simple visual
    if selected_chart == "sales":
        chart = dcc.Graph(
            figure={
                "data": [{"x": df["Category"], "y": df["Value"], "type": "bar", "name": "Sales"}],
                "layout": {"title": "Sales Overview"}
            }
        )
    elif selected_chart == "revenue":
        chart = dcc.Graph(
            figure={
                "data": [{"labels": df["Category"], "values": df["Value"], "type": "pie"}],
                "layout": {"title": "Revenue Breakdown"}
            }
        )
    else:  # forecast
        chart = dcc.Graph(
            figure={
                "data": [{"x": df["Category"], "y": [v + 5 for v in df["Value"]],
                          "type": "line", "name": "Forecast"}],
                "layout": {"title": "Forecasting"}
            }
        )

    return chart, quotes[selected_chart]

# ------------------------------------------------------------
# Run locally (optional)
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
