from dash import html, dcc
import plotly.graph_objects as go
import calendar
import itertools
import numpy as np
from xgboost import XGBRegressor
import pandas as pd
from ..callbacks.xgboost_callbacks import prepare_model_data

def create_xgboost_layout(movies_metadata):
    # Train model once
    regressor, genre_columns = prepare_model_data(movies_metadata)
    
    # Create initial plot
    genre_options = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Romance']
    budget_options = [20_000_000, 50_000_000, 100_000_000]
    
    def predict_best_release_month(genres_list, budget):
        test_rows = []
        for month in range(1, 13):
            row = [1 if col.replace("genre_", "") in genres_list else 0 for col in genre_columns]
            row += [budget, month]
            test_rows.append(row)
        
        test_df = pd.DataFrame(test_rows, columns=genre_columns + ['budget', 'release_month'])
        predicted_revenues = regressor.predict(test_df)
        return predicted_revenues
    
    predictions = {}
    for genre, budget in itertools.product(genre_options, budget_options):
        revenues = predict_best_release_month([genre], budget)
        predictions[(genre, budget)] = revenues
    
    months = list(calendar.month_name[1:])
    initial_genre = genre_options[0]
    initial_budget = budget_options[0]
    initial_data = predictions[(initial_genre, initial_budget)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=initial_data,
        mode='lines+markers',
        name=f"{initial_genre} | ${initial_budget:,}",
        hovertemplate='Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Predicted Revenue for {initial_genre} | ${initial_budget:,}",
        xaxis_title="Month",
        yaxis_title="Predicted Revenue ($)",
        height=700,
        template="plotly_white"
    )
    
    return html.Div([
        html.H1("Movie Revenue Prediction", className="text-center mb-4"),
        html.Div([
            html.Div([
                html.Label("Select Genre:"),
                dcc.Dropdown(
                    id='genre-dropdown',
                    options=[{'label': genre, 'value': genre} for genre in genre_options],
                    value=initial_genre,
                    className="mb-3"
                ),
                html.Label("Select Budget:"),
                dcc.Dropdown(
                    id='budget-dropdown',
                    options=[{'label': f"${budget//1_000_000}M", 'value': budget} for budget in budget_options],
                    value=initial_budget,
                    className="mb-3"
                ),
            ], className="col-md-4"),
            html.Div([
                dcc.Graph(id='revenue-prediction-graph', figure=fig)
            ], className="col-md-8")
        ], className="row")
    ]) 