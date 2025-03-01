"""
Dashboard Layout Module

This module defines the layout and UI components for the AllePoints dashboard.
"""

import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def create_layout(app, data_processor):
    """
    Create the layout for the dashboard application.
    
    Args:
        app (dash.Dash): The Dash application instance.
        data_processor (DataProcessor): The data processor instance.
        
    Returns:
        dash.html.Div: The main layout container.
    """
    # Register callbacks
    register_callbacks(app, data_processor)
    
    # Create the layout
    layout = dbc.Container(
        [
            # Header
            dbc.Row(
                dbc.Col(
                    html.H1("AllePoints Dashboard", className="text-center my-4"),
                    width=12
                )
            ),
            
            # Summary statistics cards
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Total Members", className="card-title"),
                                    html.H2(id="total-members", className="card-text text-center")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Members with Points", className="card-title"),
                                    html.H2(id="members-with-points", className="card-text text-center")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Total Points", className="card-title"),
                                    html.H2(id="total-points", className="card-text text-center")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Average Points", className="card-title"),
                                    html.H2(id="avg-points", className="card-text text-center")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=3
                    ),
                ]
            ),
            
            # Filters
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Filters", className="card-title"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Label("Minimum Points:"),
                                                dcc.Slider(
                                                    id="min-points-slider",
                                                    min=0,
                                                    max=200,
                                                    step=10,
                                                    value=0,
                                                    marks={i: str(i) for i in range(0, 201, 50)},
                                                )
                                            ],
                                            width=6
                                        ),
                                        dbc.Col(
                                            [
                                                html.Label("Refresh Data:"),
                                                html.Div(
                                                    dbc.Button(
                                                        "Refresh",
                                                        id="refresh-button",
                                                        color="primary",
                                                        className="mt-2"
                                                    )
                                                )
                                            ],
                                            width=6
                                        )
                                    ]
                                )
                            ]
                        ),
                        className="mb-4"
                    ),
                    width=12
                )
            ),
            
            # Points distribution chart
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Points Distribution", className="card-title"),
                                dcc.Graph(id="points-distribution-chart")
                            ]
                        ),
                        className="mb-4"
                    ),
                    width=12
                )
            ),
            
            # Members table
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Members with Points", className="card-title"),
                                dash_table.DataTable(
                                    id="members-table",
                                    columns=[
                                        {"name": "ID", "id": "id"},
                                        {"name": "Name", "id": "name"},
                                        {"name": "Phone", "id": "phone"},
                                        {"name": "Points", "id": "points"}
                                    ],
                                    page_size=10,
                                    style_table={"overflowX": "auto"},
                                    style_cell={
                                        "textAlign": "left",
                                        "padding": "10px"
                                    },
                                    style_header={
                                        "backgroundColor": "rgb(230, 230, 230)",
                                        "fontWeight": "bold"
                                    },
                                    style_data_conditional=[
                                        {
                                            "if": {"row_index": "odd"},
                                            "backgroundColor": "rgb(248, 248, 248)"
                                        }
                                    ]
                                )
                            ]
                        ),
                        className="mb-4"
                    ),
                    width=12
                )
            ),
            
            # Footer
            dbc.Row(
                dbc.Col(
                    html.Footer(
                        "AllePoints Dashboard © 2025",
                        className="text-center text-muted py-3"
                    ),
                    width=12
                )
            )
        ],
        fluid=True,
        className="px-4"
    )
    
    return layout

def register_callbacks(app, data_processor):
    """
    Register callbacks for the dashboard components.
    
    Args:
        app (dash.Dash): The Dash application instance.
        data_processor (DataProcessor): The data processor instance.
    """
    @app.callback(
        [
            dash.Output("total-members", "children"),
            dash.Output("members-with-points", "children"),
            dash.Output("total-points", "children"),
            dash.Output("avg-points", "children"),
            dash.Output("points-distribution-chart", "figure"),
            dash.Output("members-table", "data")
        ],
        [
            dash.Input("refresh-button", "n_clicks"),
            dash.Input("min-points-slider", "value")
        ]
    )
    def update_dashboard(n_clicks, min_points):
        # Fetch fresh data
        data_processor.fetch_data()
        
        # Get summary statistics
        stats = data_processor.get_summary_stats()
        
        # Get members with points above the threshold
        members_with_points = data_processor.get_members_with_points(min_points)
        
        # Create points distribution chart
        if not members_with_points.empty:
            fig = px.bar(
                members_with_points,
                x="name",
                y="points",
                title="Points by Member",
                labels={"name": "Member Name", "points": "Points"},
                color="points",
                color_continuous_scale="Viridis"
            )
        else:
            # Create empty figure if no data
            fig = px.bar(
                pd.DataFrame({"name": [], "points": []}),
                x="name",
                y="points",
                title="Points by Member (No Data)"
            )
        
        # Format numbers for display
        total_members = f"{stats['total_members']:,}"
        members_with_points_count = f"{stats['members_with_points']:,}"
        total_points = f"{stats['total_points']:,}"
        avg_points = f"{stats['avg_points']:.1f}"
        
        return (
            total_members,
            members_with_points_count,
            total_points,
            avg_points,
            fig,
            members_with_points.to_dict("records") if not members_with_points.empty else []
        ) 