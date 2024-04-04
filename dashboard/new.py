import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard.dash_app import app
from dashboard.dash_app import render_data_dashboard

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the sidebar layout
sidebar = dbc.Nav(
    [
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("Trading Journal", href="/trading-journal", active="exact"),
        dbc.NavLink("Trading History", href="/trading-history", active="exact"),
        # Add more navigation links as needed
    ],
    vertical=True,
    pills=True,
)

# Define the main content layout
content = html.Div(id="page-content")

# Define the overall app layout
app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        dbc.Row(
            [
                dbc.Col(sidebar, md=2),
                dbc.Col(content, md=10),
            ]
        ),
    ],
    fluid=True,
)

# Callback to update the page content based on the URL
@app.callback(
    dash.Output("page-content", "children"),
    [dash.Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return  render_data_dashboard()
    elif pathname == "/trading-journal":
        return html.P("This is the trading journal page")
    # Add more pages as needed


if __name__ == "__main__":
    app.run_server(debug=True)