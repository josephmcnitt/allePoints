#!/usr/bin/env python3
"""
AllePoints Dashboard Application

This is the main entry point for the AllePoints dashboard application.
It initializes the dashboard and starts the web server.
"""

import os
from dotenv import load_dotenv
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.data.data_processor import DataProcessor
from src.dashboard.layout import create_layout

# Load environment variables
load_dotenv()

# Initialize the data processor
data_processor = DataProcessor()

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "AllePoints Dashboard"

# Set up the app layout
app.layout = create_layout(app, data_processor)

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, port=port) 