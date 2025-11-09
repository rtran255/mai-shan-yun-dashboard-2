# app.py
import time
import random

import dash
from dash import html, dcc, Input, Output, no_update
import dash_bootstrap_components as dbc
import pandas as pd

# --- Use a Bootstrap theme from dash_bootstrap_components ---
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server  # required by Gunicorn / Render

# --- Example placeholder DataFrame (pandas available) ---
df_sample = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=12, freq="M"),
    "usage": [50, 60, 55, 80, 75, 90, 120, 110, 95, 85, 70, 65],
    "purchases": [60, 55, 65, 70, 90, 85, 140, 100, 100, 80, 70, 60]
})

# --- Quotes for loading overlay ---
AGGIE_QUOTES = [
    "Gig ’em, Aggies!",
    "From College Station with Maroon Pride.",
    "Keepin’ it maroon, keepin’ it strong.",
    "Whoop! Data never looked so good.",
    "Excellence. Integrity. Leadership. Loyalty. Respect. Selfless Service.",
    "Inventory efficiency — the Aggie way!"
]

# --- Header ---
header = html.Header(
    className="app-header",
    children=[
        html.Img(src="/assets/logo-placeholder.png", className="header-logo"),
        html.H1("Mai Shan Yun Inventory Intelligence Dashboard", className="app-title")
    ]
)

# --- Sidebar ---
sidebar = html.Div(
    className="sidebar",
    children=[
        html.H2("Dashboard Sections", className="sidebar-title"),
        dcc.RadioItems(
            id="graph-selector",
            options=[
                {"label": "📦 Inventory Overview", "value": "inventory"},
                {"label": "🥬 Ingredients", "value": "ingredients"},
                {"label": "🚚 Purchases & Shipments", "value": "purchases"},
                {"label": "📈 Forecasting", "value": "forecasting"},
            ],
            value="inventory",
            className="sidebar-options"
        )
    ]
)

# --- Main Content ---
main_content = html.Div(
    className="main-content",
    children=[
        dcc.Loading(
            id="loading-graph",
            type="circle",
            color="#500000",
            fullscreen=False,
            children=dcc.Graph(id="main-graph", figure={})
        ),
        html.Div(id="graph-description", className="graph-description")
    ]
)

# --- Loading Overlay ---
loading_overlay = html.Div(
    id="loading-overlay",
    children=[
        html.Div(className="spinner"),
        html.Img(src="/assets/logo-placeholder.png", className="loading-logo"),
        html.Div(id="loading-quote", className="loading-quote")
    ]
)

# --- Layout ---
app.layout = html.Div([
    loading_overlay,
    header,
    html.Div(className="content-area", children=[sidebar, main_content])
])

# --- Callbacks ---

@app.callback(
    Output("loading-overlay", "className"),
    Output("loading-quote", "children"),
    Input("graph-selector", "value"),
    prevent_initial_call=True
)
def show_loading(selected):
    """Show overlay + random Aggie quote when switching graphs"""
    quote = random.choice(AGGIE_QUOTES)
    return "active", quote


@app.callback(
    Output("main-graph", "figure"),
    Output("graph-description", "children"),
    Input("graph-selector", "value")
)
def update_graph(selected):
    """Placeholder graph logic — to be replaced with Plotly visuals later"""
    # simulate load to demonstrate loading overlay
    time.sleep(1.2)

    desc = {
        "inventory": "Overview of all inventory items and usage trends.",
        "ingredients": "Monthly ingredient usage and top/least used ingredients.",
        "purchases": "Shipment and purchase analysis by date.",
        "forecasting": "Predictive trends and restock suggestions."
    }.get(selected, "Select a view to explore inventory intelligence.")

    # For now, return an empty figure (your data & Plotly figures go here)
    fig = {}

    return fig, desc


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
