###pakage install##
###pip install dash dash-bootstrap-components pandas numpy
### Import Packages ########################################
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import pickle

### Setup ###################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Stroke Prediction Model'

### load ML model ###########################################
# with open('RFModel.pkl', 'rb') as f:
#     model = pickle.load(f)

with open('RFModel0.pkl', 'rb') as f:
    model = pickle.load(f)

### App Layout ###############################################
app.layout = html.Div([
    html.I(className="fa fa-heartbeat", style={"marginRight": "10px"}),
    html.H1("Stroke Prediction App", style={"textAlign": "center", 'color' : "#007bff", "padding": "10px",
    "border-radius": "5px"}),
    # Row 1
    dbc.Row([
        dbc.Col([
            html.Label("Gender:"),
            dcc.Dropdown(id="gender", options=[
                {"label": "Male", "value": 1},
                {"label": "Female", "value": 0}
            ], value=0)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"}),  # First column (50% width of the row)
        dbc.Col([
            html.Label("Age:"),
            html.Br(),
            dcc.Input(id="age", type="number", value=25)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"})  # Second column (50% width of the row)
    ]),
    html.Br(),
    # Row 2
    dbc.Row([
        dbc.Col([
            html.Label("Hypertension:"),
            dcc.Dropdown(id="hypertension", options=[
                {"label": "Yes", "value": 1},
                {"label": "No", "value": 0}
            ], value=0)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"}),
        dbc.Col([
            html.Label("Heart Disease:"),
            dcc.Dropdown(id="heart_disease", options=[
                {"label": "Yes", "value": 1},
                {"label": "No", "value": 0}
            ], value=0)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"})
    ]),
    html.Br(),
    # Row 3
    dbc.Row([
        dbc.Col([
            html.Label("Ever Married:"),
            dcc.Dropdown(id="ever_married", options=[
                {"label": "Yes", "value": 1},
                {"label": "No", "value": 0}
            ], value=0)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"}),
        dbc.Col([
            html.Label("Work Type:"),
            dcc.Dropdown(id="work_type", options=[
                {"label": "Private", "value": 0},
                {"label": "Self-employed", "value": 1},
                {"label": "Government", "value": 2},
                {"label": "Children", "value": 3},
                {"label": "Never worked", "value": 4}
            ], value=0)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"})
    ]),
    html.Br(),
    # Row 4
    dbc.Row([
        dbc.Col([
            html.Label("Residence Type:"),
            dcc.Dropdown(id="residence_type", options=[
                {"label": "Urban", "value": 0},
                {"label": "Rural", "value": 1}
            ], value=0)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"}),
        dbc.Col([
            html.Label("Average Glucose Level:"),
            html.Br(),
            dcc.Input(id="avg_glucose_level", type="number", value=100)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"})
    ]),
    html.Br(),
    # Row 5
    dbc.Row([
        dbc.Col([
            html.Label("BMI:"),
            html.Br(),
            dcc.Input(id="bmi", type="number", value=25)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"}),
        dbc.Col([
            html.Label("Smoking Status:"),
            dcc.Dropdown(id="smoking_status", options=[
                {"label": "Never smoked", "value": 0},
                {"label": "Formerly smoked", "value": 1},
                {"label": "Smokes", "value": 2},
                {"label": "Unknown", "value": 3}
            ], value=0)
        ], width=6, style={"border": "1px solid #ddd", "borderRadius": "5px", "padding": "10px"})
    ]),
    html.Br(),
    
    html.Div([
    html.Button("Predict", id="predict-button", n_clicks=0, style={
    "backgroundColor": "#007bff",
    "color": "white",
    "border": "none",
    "borderRadius": "5px",
    "padding": "10px 20px",
    "cursor": "pointer",
    "transition": "background-color 0.3s ease"
}),
    html.Br(),
    html.Div(id="prediction-output", style={
    "fontSize": "18px", 
    "color": "#28a745",  # Success green
    "fontWeight": "bold",
    "textAlign": "center",
    "marginTop": "20px"
})
    ], style={"textAlign": "center", "marginTop": "20px", "padding": "10px"}),
    html.Div(id="feature-summary"),  # For live updates of feature inputs

], style={"fontFamily": "'Roboto', sans-serif"})

# Prediction logic
@app.callback(
    Output("prediction-output", "children"),  # Update the prediction output
    Input("predict-button", "n_clicks"),      # Trigger on button clicks
    [Input("gender", "value"),
     Input("age", "value"),
     Input("hypertension", "value"),
     Input("heart_disease", "value"),
     Input("ever_married", "value"),
     Input("work_type", "value"),
     Input("residence_type", "value"),
     Input("avg_glucose_level", "value"),
     Input("bmi", "value"),
     Input("smoking_status", "value")]
)

def predict_stroke(n_clicks, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status):
    if n_clicks is None or n_clicks == 0:
        return "Click the Predict button to get the result."

    # Make prediction
    features = pd.DataFrame([[gender, age, hypertension, heart_disease, ever_married, work_type,
                              residence_type, avg_glucose_level, bmi, smoking_status]],
                            columns=['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 
                                     'work_type', 'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'])
    prediction = model.predict(features)[0]
    return f"Stroke Prediction: {'Yes' if prediction == 1 else 'No'}"


# Dictionary for Work Type mapping
work_type_labels = {
    0: "Private",
    1: "Self-employed",
    2: "Government",
    3: "Children",
    4: "Never worked"
}

smoking_status_labels = {
    0: "Never smoked",
    1: "Formerly smoked",
    2: "Smokes",
    3: "Unknown"}

@app.callback(
    Output("feature-summary", "children"),  # Update a feature summary section
    [Input("gender", "value"),
     Input("age", "value"),
     Input("hypertension", "value"),
     Input("heart_disease", "value"),
     Input("ever_married", "value"),
     Input("work_type", "value"),
     Input("residence_type", "value"),
     Input("avg_glucose_level", "value"),
     Input("bmi", "value"),
     Input("smoking_status", "value")]
)
def update_feature_summary(gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status):
    # Build a summary of the current feature values
    # Convert numeric values to labels using the dictionary
    work_type_label = work_type_labels.get(work_type, "Unknown")
    smoking_status_label = smoking_status_labels.get(smoking_status, "Unknown")
    return f"""
    Gender: {'Male' if gender == 1 else 'Female'}, Age: {age}, 
    Hypertension: {'Yes' if hypertension == 1 else 'No'}, Heart Disease: {'Yes' if heart_disease == 1 else 'No'}, 
    Married: {'Yes' if ever_married == 1 else 'No'}, Work Type: {work_type_label}, 
    Residence: {'Urban' if residence_type == 0 else 'Rural'}, Glucose Level: {avg_glucose_level}, 
    BMI: {bmi}, Smoking Status: {smoking_status_label}
    """

    
### Run the App ###############################################
if __name__ == '__main__':
    app.run_server(debug=True)