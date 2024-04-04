import plotly.express as px
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd


import base64
import io

from database.db_utils import fetch_data  # Assuming you have this function to fetch data from the database
from processing.data_processor import  data_processor_and_db_insert  # Import your data processing and DB insert functions

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define custom CSS styles for further enhancing the dashboard
CUSTOM_CSS = {
    "navbar": {
        "background-color": "#f8f9fa",
    },
    "nav-title": {
        "font-weight": "bold",
        "font-size": "20px",
        "color": "#007BFF",  # Adjust the color to match LUX theme or your preference
    },
    "upload-box": {
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '2px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'padding': '10px',
        'fontSize': '16px',
    }
}

# Define enhanced custom CSS for the drag-and-drop area
CUSTOM_CSS['upload-box'] = {
    'width': 'auto',
    'minHeight': '100px',
    'lineHeight': '60px',
    'borderWidth': '2px',
    'borderStyle': 'dashed',
    'borderRadius': '10px',
    'textAlign': 'center',
    'margin': '20px auto',  # Centering the box
    'padding': '20px',
    'fontSize': '16px',
    'color': '#888',  # Subtle text color
    'backgroundColor': '#fafafa',  # Soft background color
    'cursor': 'pointer',  # Change cursor to indicate clickable area
    'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.1)',  # Soft shadow for depth
}


# App layout
def render_data_dashboard():

    return dbc.Container([
        # Navigation Bar
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="#")),
                dbc.NavItem(dbc.NavLink("Documentation", href="#")),
                dbc.NavItem(dbc.NavLink("About", href="#")),
            ],
            brand="Data Insights Dashboard",
            brand_href="#",
            color="primary",
            dark=True,
            fluid=True,
        ),
        
        html.Hr(),
        
        # Dashboard Introduction
        dbc.Row([
            dbc.Col(html.H3("Welcome to Your Data Insights Dashboard",
                            style={'textAlign': 'center'}),
                    width=12),
        ]),
        
        html.Hr(),
        
        # File Upload Section
        dbc.Row([
            dbc.Col([
                html.H5("Upload Your Data Here", className="text-center"),
                html.P("Supported file formats: Excel (.xlsx). Drag and Drop or Click to Select Files.",
                       className="text-center"),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        html.Span("Drag and Drop or ", style={'fontSize': '18px'}),
                        html.A('Select Files', style={'color': '#007bff', 'cursor': 'pointer'}),
                    ]),
                    style=CUSTOM_CSS['upload-box'],
                    multiple=True
                ),
                html.Div(id='output-data-upload'),
            ], width=12),
        ]),
        
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='line-graph'),
            ], width=12),
        ]),
        # Add the Interval component here
        dcc.Interval(
            id='interval-component',
            interval=1*60*1000,  # Interval set to 1 minute
            n_intervals=0
        ),
    ])
app.layout = render_data_dashboard()
# Callback for file upload
@callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(list_of_contents, list_of_names):
    print(list_of_contents)
    
    if list_of_contents is not None:
        children = []
        for content, name in zip(list_of_contents, list_of_names):
            df = parse_contents(content, name)
            
            if df is not None:
                print(df)
                # Process and insert data into the database
                data_processor_and_db_insert(df)
                children.append(html.Div(f'Processed file: {name}'))
        return children
    return "No file uploaded."

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'xlsx' in filename:
            # Assume that the user uploaded an Excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df
    except Exception as e:
        print(e)
        return None

"""@callback(
    Output('line-graph', 'figure'),
    [Input('upload-data', 'contents'),  # Triggered when a new file is uploaded
     Input('interval-component', 'n_intervals')]  # Triggered at regular intervals
)
def update_graph(list_of_contents, n):
    # Fetch data from the database
    df = fetch_data()  # Implement this function to fetch data from your database

    # Create a line graph
    fig = px.line(df, x='date_utc_in', y='realized_profit', markers=True)

    return fig"""

@callback(
    Output('line-graph', 'figure'),
    [Input('upload-data', 'contents'),  # Triggered when a new file is uploaded
     Input('interval-component', 'n_intervals')]  # Triggered at regular intervals
)
def update_graph(list_of_contents, n):
    # Fetch data from the database
    df = fetch_data()  # Implement this function to fetch data from your database
    

    # Create a histogram/bar chart
    fig = px.bar(df,  y='realized_profit')


    # Update the bar color based on the sign of the values
    fig.update_traces(marker_color=df['realized_profit'].apply(lambda x: '#2ECC71' if x >= 0 else '#E74C3C'))
    #specific_ticks = df['date_utc_in'].tolist()
    #specific_ticks = df['tick_column'].dt.strftime('%Y-%m-%d %H:%M').tolist()
    #fig.update_xaxes(tickvals=specific_ticks)
  
    
    fig.update_xaxes(tickangle=-45)


    return fig

if __name__ == '__main__':
    
    app.run_server(debug=True)