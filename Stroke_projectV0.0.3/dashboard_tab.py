import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def get_dashboard_tab(stroke_visualize):
    # Donut charts for categorical features
    cat_features = ['gender', 'smoking_status', 'work_type', 'ever_married', 'residence_type']
    donut_charts = []

    for feature in cat_features:
        feature_counts = stroke_visualize.groupby([feature, 'stroke']).size().unstack().fillna(0)
        feature_counts = feature_counts[1] / feature_counts.sum(axis=1) * 100  # Percentage of stroke cases

        fig = px.pie(
            names=feature_counts.index,
            values=feature_counts,
            title=f"Stroke Cases by {feature}",
            hole=0,
            labels={feature: feature, 'value': 'Percentage'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        donut_charts.append(fig)

    # Bar charts for stroke by age group, glucose category, and BMI category
    age_stroke_fig = px.bar(
        stroke_visualize.groupby('age_group')['stroke'].mean().reset_index(),
        x='age_group',
        y='stroke',
        title='Stroke by Age Group',
        labels={'stroke': 'Stroke Rate', 'age_group': 'Age Group'},
        color_discrete_sequence=['#636EFA']
    )
    age_stroke_fig.update_layout(xaxis_tickangle=-45)

    glucose_stroke_fig = px.bar(
        stroke_visualize.groupby('glucose_category')['stroke'].mean().reset_index(),
        x='glucose_category',
        y='stroke',
        title='Glucose Category vs Stroke',
        labels={'stroke': 'Stroke Rate', 'glucose_category': 'Glucose Category'},
        color_discrete_sequence=['#EF553B']
    )

    bmi_stroke_fig = px.bar(
        stroke_visualize.groupby('bmi_category')['stroke'].mean().reset_index(),
        x='bmi_category',
        y='stroke',
        title='BMI Category vs Stroke',
        labels={'stroke': 'Stroke Rate', 'bmi_category': 'BMI Category'},
        color_discrete_sequence=['#00CC96']
    )

    # Layout: Donut charts in 2 rows and 3 columns
    donut_rows = []
    for i in range(0, len(donut_charts), 3):
        donut_rows.append(
            dbc.Row([
                dbc.Col(dcc.Graph(figure=donut_charts[i]), width=4),
                dbc.Col(dcc.Graph(figure=donut_charts[i+1]), width=4) if i+1 < len(donut_charts) else dbc.Col(),
                dbc.Col(dcc.Graph(figure=donut_charts[i+2]), width=4) if i+2 < len(donut_charts) else dbc.Col()
            ])
        )

    # Full-width bar chart for age group
    bar_row = dbc.Row([dbc.Col(dcc.Graph(figure=age_stroke_fig), width=12)], className="mb-4")

    # Side-by-side bar charts for glucose and BMI categories
    side_by_side_bars = dbc.Row([
        dbc.Col(dcc.Graph(figure=glucose_stroke_fig), width=6),
        dbc.Col(dcc.Graph(figure=bmi_stroke_fig), width=6)
    ])

    # Grouping data
    grouped_data = stroke_visualize.groupby(['age_group', 'gender', 'bmi_category']).size().reset_index(name='count')

    # Equivalent Plotly plot with facets
    bmi_cat_plot = px.bar(
        grouped_data,
        x="age_group",
        y="count",
        color="bmi_category",
        facet_col="gender",
        title="Relation Between Age Group, Gender, and BMI Category",
        labels={"count": "Number of People", "age_group": "Age Group"},
        barmode="group"
    )

    # Optional: Update layout for better spacing
    bmi_cat_plot.update_layout(margin=dict(t=80), height=600)
    bmi_cat_plot.update_xaxes(tickangle=45)

    # Combine all components
    return html.Div([
        html.H2("Stroke Prediction Dashboard", style={"textAlign": "center", "marginTop": "30px", "color": "#007bff"}),
        *donut_rows,
        bar_row,
        side_by_side_bars,
        dcc.Graph(id='bmi-cat-plot', figure=bmi_cat_plot),
    ])