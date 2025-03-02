"""
Dashboard Layout Module

This module defines the layout and UI components for the AllePoints dashboard.
"""

import dash
from dash import html, dcc, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

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
            
            # Phone Number Search Section
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Search by Phone Number", className="card-title"),
                                    html.Div(
                                        [
                                            dbc.Input(
                                                id="phone-search-input",
                                                type="text",
                                                placeholder="Enter phone number (e.g., 555-123-4567)",
                                                className="mb-2"
                                            ),
                                            dbc.Button(
                                                "Search",
                                                id="phone-search-button",
                                                color="primary",
                                                className="mb-2"
                                            ),
                                            dbc.Spinner(
                                                html.Div(id="phone-search-loading"),
                                                color="primary",
                                                type="grow",
                                                size="sm"
                                            )
                                        ]
                                    )
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=12
                    )
                ]
            ),
            
            # Member Details Section (hidden by default)
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Member Details", className="card-title"),
                                html.Div(id="member-details-content", style={"display": "none"})
                            ]
                        ),
                        id="member-details-card",
                        className="mb-4",
                        style={"display": "none"}
                    ),
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
                        width=12, md=4
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
                        width=12, md=4
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
                        width=12, md=4
                    )
                ]
            ),
            
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Average Points per Member", className="card-title"),
                                    html.H2(id="avg-points", className="card-text text-center")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=12, md=6
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Filter by Minimum Points", className="card-title"),
                                    dcc.Slider(
                                        id="min-points-slider",
                                        min=0,
                                        max=500,
                                        step=50,
                                        value=0,
                                        marks={i: str(i) for i in range(0, 501, 100)},
                                        className="my-4"
                                    ),
                                    dbc.Button(
                                        "Refresh Data",
                                        id="refresh-button",
                                        color="primary",
                                        className="mt-2"
                                    )
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=12, md=6
                    )
                ]
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
                                html.H4("Members List", className="card-title"),
                                dash_table.DataTable(
                                    id="members-table",
                                    columns=[
                                        {"name": "ID", "id": "id"},
                                        {"name": "Name", "id": "name"},
                                        {"name": "Phone", "id": "phone"},
                                        {"name": "Points", "id": "points"}
                                    ],
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
                                    ],
                                    page_size=10
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
                        "AllePoints Dashboard © 2023",
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
    Register callbacks for the dashboard application.
    
    Args:
        app (dash.Dash): The Dash application instance.
        data_processor (DataProcessor): The data processor instance.
    """
    @app.callback(
        [
            Output("total-members", "children"),
            Output("members-with-points", "children"),
            Output("total-points", "children"),
            Output("avg-points", "children"),
            Output("points-distribution-chart", "figure"),
            Output("members-table", "data")
        ],
        [
            Input("refresh-button", "n_clicks"),
            Input("min-points-slider", "value")
        ]
    )
    def update_dashboard(n_clicks, min_points):
        """
        Update the dashboard with fresh data.
        
        Args:
            n_clicks (int): Number of times the refresh button has been clicked.
            min_points (int): Minimum number of points to filter by.
            
        Returns:
            tuple: Tuple containing updated values for dashboard components.
        """
        # Fetch fresh data
        data_processor.fetch_data()
        
        # Get summary statistics
        stats = data_processor.get_summary_stats()
        
        # Get filtered members data
        members_data = data_processor.get_members_with_points(min_points)
        
        # Create points distribution chart
        if not members_data.empty:
            fig = px.histogram(
                members_data,
                x="points",
                nbins=20,
                title="Distribution of Points",
                labels={"points": "Points", "count": "Number of Members"},
                color_discrete_sequence=["#007BFF"]
            )
            fig.update_layout(
                xaxis_title="Points",
                yaxis_title="Number of Members",
                bargap=0.1
            )
        else:
            fig = px.histogram(
                pd.DataFrame({"points": [0]}),
                x="points",
                title="Distribution of Points (No Data)",
                labels={"points": "Points", "count": "Number of Members"},
                color_discrete_sequence=["#007BFF"]
            )
        
        # Format numbers for display
        total_members = f"{stats['total_members']:,}"
        members_with_points = f"{stats['members_with_points']:,}"
        total_points = f"{stats['total_points']:,}"
        avg_points = f"{stats['avg_points']:.1f}"
        
        # Return updated values
        return (
            total_members,
            members_with_points,
            total_points,
            avg_points,
            fig,
            members_data.to_dict("records") if not members_data.empty else []
        )
    
    @app.callback(
        [
            Output("member-details-card", "style"),
            Output("member-details-content", "style"),
            Output("member-details-content", "children"),
            Output("phone-search-loading", "children")
        ],
        [Input("phone-search-button", "n_clicks")],
        [State("phone-search-input", "value")],
        prevent_initial_call=True
    )
    def search_member_by_phone(n_clicks, phone_number):
        """
        Search for a member by phone number and display the results.
        
        Args:
            n_clicks (int): Number of times the search button has been clicked.
            phone_number (str): The phone number to search for.
            
        Returns:
            tuple: Tuple containing updated values for member details components.
        """
        if not phone_number:
            return {"display": "none"}, {"display": "none"}, [], ""
        
        # Search for the member
        member_data = data_processor.search_by_phone(phone_number)
        
        if not member_data:
            return (
                {"display": "block"},
                {"display": "block"},
                html.Div([
                    html.P("No member found with this phone number.", className="text-danger")
                ]),
                ""
            )
        
        # Create member details content
        details_content = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5("Member Information", className="mb-3"),
                    html.Table([
                        html.Tr([
                            html.Td("Name:", className="font-weight-bold pr-3"),
                            html.Td(member_data.get("name", "N/A"))
                        ]),
                        html.Tr([
                            html.Td("Member ID:", className="font-weight-bold pr-3"),
                            html.Td(member_data.get("id", "N/A"))
                        ]),
                        html.Tr([
                            html.Td("Phone:", className="font-weight-bold pr-3"),
                            html.Td(member_data.get("phone", "N/A"))
                        ]),
                        html.Tr([
                            html.Td("Email:", className="font-weight-bold pr-3"),
                            html.Td(member_data.get("email", "N/A"))
                        ])
                    ], className="table table-borderless")
                ], md=6),
                dbc.Col([
                    html.H5("Points Information", className="mb-3"),
                    html.Table([
                        html.Tr([
                            html.Td("Current Points:", className="font-weight-bold pr-3"),
                            html.Td(f"{member_data.get('points', 0):,}")
                        ])
                    ], className="table table-borderless"),
                    dbc.Progress(
                        value=min(member_data.get("points", 0), 1000),
                        max=1000,
                        color="success",
                        className="mb-3",
                        style={"height": "30px"}
                    ),
                    html.P(f"Progress toward 1,000 points: {min(member_data.get('points', 0) / 10, 100):.1f}%")
                ], md=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Raw Data", className="mb-3"),
                    dcc.Markdown(f"```json\n{json.dumps(member_data, indent=2)}\n```")
                ])
            ])
        ])
        
        return {"display": "block"}, {"display": "block"}, details_content, "" 