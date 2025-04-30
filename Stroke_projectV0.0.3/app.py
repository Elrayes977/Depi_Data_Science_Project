# app.py
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dashboard_tab import get_dashboard_tab
from prediction_tab import get_prediction_tab, register_prediction_callbacks
import dash_bootstrap_components as dbc

stroke_visualize = pd.read_csv('stroke_data.csv')

# Create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Stroke Prediction App"

# Layout
app.layout = html.Div([
    html.H1("Stroke Prediction App", style={"textAlign": "center", "marginTop": "20px", "color": "#007bff"}),
    dcc.Tabs(id="tabs", value='tab-dashboard', children=[
        dcc.Tab(label="Dashboard", value="tab-dashboard"),
        dcc.Tab(label="Prediction", value="tab-prediction")
    ]),
    html.Div(id="tabs-content")
])

# Callback to switch tabs
@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "tab-dashboard":
        return get_dashboard_tab(stroke_visualize)
    elif tab == "tab-prediction":
        return get_prediction_tab()

# Register prediction tab callbacks
register_prediction_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
