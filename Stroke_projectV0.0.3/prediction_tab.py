import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pickle

# Load the trained model and feature names
# model_pipeline = joblib.load('rf_model.pkl')
# expected_columns = joblib.load('columns.pkl')

with open('rf_model.pkl', 'rb') as f:
    model_pipeline = pickle.load(f)

with open('columns.pkl', 'rb') as f:
    expected_columns = pickle.load(f)

# Option dictionaries
work_type_labels = {0: "Private", 1: "Self-employed", 2: "Government", 3: "Children", 4: "Never worked"}
smoking_status_labels = {0: "Never smoked", 1: "Formerly smoked", 2: "Smokes", 3: "Unknown"}

def get_prediction_tab():

    # Define the layout of the app
    return dbc.Container([
    html.H2("Stroke Prediction", className="text-center mb-4"),

    dbc.Row([
        # Left column (5 fields)
        dbc.Col([
            dbc.Label("Gender"),
            dcc.Dropdown(
                id="gender",
                options=[{"label": "Male", "value": "Male"}, {"label": "Female", "value": "Female"}],
                placeholder="Select Gender",
                className="mb-3"
            ),

            dbc.Label("Age"),
            dbc.Input(id="age", type="number", placeholder="Enter Age", className="mb-3"),

            dbc.Label("Hypertension"),
            dcc.Dropdown(
                id="hypertension",
                options=[{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
                placeholder="Select Hypertension",
                className="mb-3"
            ),

            dbc.Label("Heart Disease"),
            dcc.Dropdown(
                id="heart_disease",
                options=[{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
                placeholder="Select Heart Disease",
                className="mb-3"
            ),

            dbc.Label("Ever Married"),
            dcc.Dropdown(
                id="ever_married",
                options=[{"label": "No", "value": "No"}, {"label": "Yes", "value": "Yes"}],
                placeholder="Select Ever Married",
                className="mb-3"
            ),
        ], width=6),

        # Right column (5 fields)
        dbc.Col([
            dbc.Label("Work Type"),
            dcc.Dropdown(
                id="work_type",
                options=[
                    {"label": "Private", "value": "Private"},
                    {"label": "Self-employed", "value": "Self-employed"},
                    {"label": "Govt_job", "value": "Govt_job"},
                    {"label": "children", "value": "children"},
                    {"label": "Never_worked", "value": "Never_worked"},
                ],
                placeholder="Select Work Type",
                className="mb-3"
            ),

            dbc.Label("Residence Type"),
            dcc.Dropdown(
                id="residence_type",
                options=[{"label": "Urban", "value": "Urban"}, {"label": "Rural", "value": "Rural"}],
                placeholder="Select Residence Type",
                className="mb-3"
            ),

            dbc.Label("Average Glucose Level"),
            dbc.Input(
                id="avg_glucose_level",
                type="number",
                placeholder="Enter Average Glucose Level",
                className="mb-3"
            ),

            dbc.Label("BMI"),
            dbc.Input(id="bmi", type="number", placeholder="Enter BMI", className="mb-3"),

            dbc.Label("Smoking Status"),
            dcc.Dropdown(
                id="smoking_status",
                options=[
                    {"label": "never smoked", "value": "never smoked"},
                    {"label": "formerly smoked", "value": "formerly smoked"},
                    {"label": "smokes", "value": "smokes"},
                    {"label": "Unknown", "value": "Unknown"},
                ],
                placeholder="Select Smoking Status",
                className="mb-3"
            ),
        ], width=6),
    ]),

    # Predict Button
    dbc.Row(
        dbc.Col(
            dbc.Button("Predict Stroke", id="predict_button", color="primary", className="mt-3"),
            className="text-center"
        )
    ),

    # Output Display
    dbc.Row(
        dbc.Col(
            html.Div(id="prediction_output", className="mt-4 text-center"),
        )
    )
], fluid=True)

# Define the callback to update the prediction
def register_prediction_callbacks(app):
    @app.callback(
        Output("prediction_output", "children"),
        Input("predict_button", "n_clicks"),
        [
            State("gender", "value"),
            State("age", "value"),
            State("hypertension", "value"),
            State("heart_disease", "value"),
            State("ever_married", "value"),
            State("work_type", "value"),
            State("residence_type", "value"),
            State("avg_glucose_level", "value"),
            State("bmi", "value"),
            State("smoking_status", "value"),
        ],
    )
    def update_prediction(n_clicks, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status):
        if n_clicks is None:
            return ""
        # Prepare the input data
        input_data = pd.DataFrame(
            [{
                "gender": gender,
                "age": age,
                "hypertension": hypertension,
                "heart_disease": heart_disease,
                "ever_married": ever_married,
                "work_type": work_type,
                "residence_type" : residence_type, 
                "avg_glucose_level" : avg_glucose_level, 
                "bmi" : bmi, 
                "smoking_status" : smoking_status
            }]
        )
        # Predict using pipeline
        prediction = model_pipeline.predict(input_data)[0]
        prob = model_pipeline.predict_proba(input_data)[0][1]

        return f"Prediction: {'Stroke' if prediction else 'No Stroke'} (Probability: {prob:.2f})"
 
