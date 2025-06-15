from dash import html, dcc
import plotly.graph_objects as go
import itertools
import calendar
from ..ML_data import load_ml_data, predict_best_release_month

def create_machine_learning_layout():
    # Load ML data
    ml_data = load_ml_data()
    
    # Generate predictions for all combinations
    predictions = {}
    for genre, budget in itertools.product(ml_data['genre_options'], ml_data['budget_options']):
        best_month, revenues = predict_best_release_month(
            ml_data['model'],
            ml_data['genre_columns'],
            [genre],
            budget
        )
        predictions[(genre, budget)] = revenues
    
    # Create initial figure
    initial_genre = ml_data['genre_options'][0]
    initial_budget = ml_data['budget_options'][0]
    initial_data = predictions[(initial_genre, initial_budget)]
    
    fig = go.Figure()
    
    trace = go.Scatter(
        x=ml_data['months'],
        y=initial_data,
        mode='lines+markers',
        name=f"{initial_genre} | ${initial_budget:,}",
        marker=dict(size=8, color='blue'),
        line=dict(color='royalblue'),
        hovertemplate='Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    )
    fig.add_trace(trace)
    
    # Create genre buttons
    genre_buttons = []
    for genre in ml_data['genre_options']:
        new_y = predictions[(genre, initial_budget)]
        genre_buttons.append(dict(
            label=genre,
            method='update',
            args=[
                {'y': [new_y]},
                {'title': f'Predicted Revenue for {genre} | ${initial_budget:,}'}
            ]
        ))
    
    # Create budget buttons
    budget_buttons = []
    for budget in ml_data['budget_options']:
        new_y = predictions[(initial_genre, budget)]
        budget_buttons.append(dict(
            label=f"${budget//1_000_000}M",
            method='update',
            args=[
                {'y': [new_y]},
                {'title': f'Predicted Revenue for {initial_genre} | ${budget:,}'}
            ]
        ))
    
    # Update layout
    fig.update_layout(
        title=f"Predicted Revenue for {initial_genre} | ${initial_budget:,}",
        xaxis_title="Month",
        yaxis_title="Predicted Revenue ($)",
        updatemenus=[
            dict(
                buttons=genre_buttons,
                direction="down",
                showactive=True,
                x=0.05,
                xanchor="left",
                y=1.2,
                yanchor="top",
                pad={"r": 10, "t": 10},
                name="genre"
            ),
            dict(
                buttons=budget_buttons,
                direction="down",
                showactive=True,
                x=0.35,
                xanchor="left",
                y=1.2,
                yanchor="top",
                pad={"r": 10, "t": 10},
                name="budget"
            ),
        ],
        height=700,
        template="plotly_white",
        hovermode='closest'
    )
    
    return html.Div([
        html.H1('Movie Revenue Prediction', className='text-2xl font-bold mb-4'),
        html.Div([
            html.P(
                'This visualization shows the predicted revenue for movies based on their genre and budget across different release months. Use the dropdowns above the chart to explore different combinations.',
                className='mb-4'
            ),
            dcc.Graph(figure=fig, id='revenue-prediction-plot')
        ], className='bg-gray-800 p-4 rounded-lg')
    ], className='p-4') 