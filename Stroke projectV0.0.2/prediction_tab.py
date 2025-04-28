# prediction_tab.py
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pickle

with open('RFModel.pkl', 'rb') as f:
    model = pickle.load(f)

# Option dictionaries
work_type_labels = {0: "Private", 1: "Self-employed", 2: "Government", 3: "Children", 4: "Never worked"}
smoking_status_labels = {0: "Never smoked", 1: "Formerly smoked", 2: "Smokes", 3: "Unknown"}

def get_prediction_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([html.Label("Gender:"), dcc.Dropdown(id="gender", options=[
                    {"label": "Male", "value": 1}, {"label": "Female", "value": 0}
                ], value=0)]),
                html.Br(),
                dbc.Row([html.Label("Hypertension:"), dcc.Dropdown(id="hypertension", options=[
                    {"label": "Yes", "value": 1}, {"label": "No", "value": 0}
                ], value=0)]),
                html.Br(),
                dbc.Row([html.Label("Ever Married:"), dcc.Dropdown(id="ever_married", options=[
                    {"label": "Yes", "value": 1}, {"label": "No", "value": 0}
                ], value=0)]),
                html.Br(),
                dbc.Row([html.Label("Residence Type:"), dcc.Dropdown(id="residence_type", options=[
                    {"label": "Urban", "value": 0}, {"label": "Rural", "value": 1}
                ], value=0)]),
                html.Br(),
                dbc.Row([html.Label("BMI:"), dcc.Input(id="bmi", type="number", value=25)])
            ], width=6),

            dbc.Col([
                dbc.Row([html.Label("Age:"), dcc.Input(id="age", type="number", value=25)]),
                html.Br(),
                dbc.Row([html.Label("Heart Disease:"), dcc.Dropdown(id="heart_disease", options=[
                    {"label": "Yes", "value": 1}, {"label": "No", "value": 0}
                ], value=0)]),
                html.Br(),
                dbc.Row([html.Label("Work Type:"), dcc.Dropdown(id="work_type", options=[
                    {"label": "Private", "value": 0}, {"label": "Self-employed", "value": 1},
                    {"label": "Government", "value": 2}, {"label": "Children", "value": 3},
                    {"label": "Never worked", "value": 4}
                ], value=0)]),
                html.Br(),
                dbc.Row([html.Label("Avg Glucose Level:"), dcc.Input(id="avg_glucose_level", type="number", value=100)]),
                html.Br(),
                dbc.Row([html.Label("Smoking Status:"), dcc.Dropdown(id="smoking_status", options=[
                    {"label": "Never smoked", "value": 0}, {"label": "Formerly smoked", "value": 1},
                    {"label": "Smokes", "value": 2}, {"label": "Unknown", "value": 3}
                ], value=0)])
            ], width=6),
        ]),
        html.Br(),

        html.Div([
            html.Button("Predict", id="predict-button", n_clicks=0, className="btn btn-primary", 
                        style={
                        "backgroundColor": "#007bff",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "padding": "10px 20px",
                        "cursor": "pointer",
                        "transition": "background-color 0.3s ease"
                    }),
            html.Div(id="prediction-output", style={"marginTop": "20px", "textAlign": "center", "fontWeight": "bold", "color": "#007bff"}),
            html.Div(id="feature-summary", style={"marginTop": "10px", "fontSize": "16px", "textAlign": "center"})
        ], style={"textAlign": "center", "marginTop": "20px", "padding": "10px"})
    ])

# Prediction Callback
def register_prediction_callbacks(app):
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-button", "n_clicks"),
        State("gender", "value"), State("age", "value"), State("hypertension", "value"),
        State("heart_disease", "value"), State("ever_married", "value"), State("work_type", "value"),
        State("residence_type", "value"), State("avg_glucose_level", "value"),
        State("bmi", "value"), State("smoking_status", "value")
    )
    def predict(n_clicks, gender, age, hypertension, heart_disease, ever_married, work_type,
                residence_type, avg_glucose_level, bmi, smoking_status):
        if not n_clicks:
            return "Click the Predict button to get the result."
        features = pd.DataFrame([[gender, age, hypertension, heart_disease, ever_married, work_type,
                                  residence_type, avg_glucose_level, bmi, smoking_status]],
                                columns=['gender', 'age', 'hypertension', 'heart_disease', 'ever_married',
                                         'work_type', 'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'])
        prediction = model.predict(features)[0]
        return f"Stroke Prediction: {'Yes' if prediction == 1 else 'No'}"

    @app.callback(
        Output("feature-summary", "children"),
        [Input("gender", "value"), Input("age", "value"), Input("hypertension", "value"),
         Input("heart_disease", "value"), Input("ever_married", "value"), Input("work_type", "value"),
         Input("residence_type", "value"), Input("avg_glucose_level", "value"),
         Input("bmi", "value"), Input("smoking_status", "value")]
    )
    def update_summary(gender, age, hypertension, heart_disease, ever_married, work_type,
                       residence_type, avg_glucose_level, bmi, smoking_status):
        return f"""
        Gender: {'Male' if gender == 1 else 'Female'}, Age: {age}, Hypertension: {'Yes' if hypertension else 'No'},
        Heart Disease: {'Yes' if heart_disease else 'No'}, Married: {'Yes' if ever_married else 'No'},
        Work Type: {work_type_labels.get(work_type)}, Residence: {'Urban' if residence_type == 0 else 'Rural'},
        Glucose: {avg_glucose_level}, BMI: {bmi}, Smoking: {smoking_status_labels.get(smoking_status)}
        """
