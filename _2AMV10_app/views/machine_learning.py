from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
import itertools
import calendar
from ..ML_data import load_ml_data, predict_best_release_month

def create_machine_learning_layout():
    # Load ML data
    ml_data = load_ml_data()

    # Initial figure setup
    initial_genre = ml_data['genre_options'][0]
    budgets = list(range(10_000_000, 110_000_000, 10_000_000))
    initial_budget = budgets[0]

    best_month, initial_data = predict_best_release_month(
        ml_data['model'], ml_data['genre_columns'], [initial_genre], initial_budget
    )

    fig = go.Figure(
        go.Scatter(
            x=ml_data['months'],
            y=initial_data,
            mode='lines+markers',
            marker=dict(size=8, color='blue'),
            line=dict(color='royalblue'),
            hovertemplate='Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        )
    )

    fig.update_layout(
        title=f"Predicted Revenue for {initial_genre} | ${initial_budget:,}",
        xaxis_title="Month",
        yaxis_title="Predicted Revenue ($)",
        height=300,
        template="plotly_white",
        hovermode='closest'
    )

    return html.Div([
        html.H2('Movie Revenue Prediction', style={"marginBottom": "10px", "fontWeight": "bold", "placement": "center"}),
        html.Div([
            html.Label("Select Genre:", className="font-semibold"),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': genre, 'value': genre} for genre in ml_data['genre_options']],
                value=initial_genre
            ),
            html.Label("Select Budget:", className="font-semibold mt-4"),
            dcc.Slider(
                id='budget-slider',
                min=10_000_000,
                max=100_000_000,
                step=10_000_000,
                value=initial_budget,
                marks={budget: f"${budget//1_000_000}M" for budget in budgets},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dcc.Graph(figure=fig, id='ML_plot')
        ], className='bg-gray-800 p-4 rounded-lg')
    ], className='p-4')

@callback(
    Output('ML_plot', 'figure'),
    Input('genre-dropdown', 'value'),
    Input('budget-slider', 'value')
)
def update_plot(selected_genre, selected_budget):
    ml_data = load_ml_data()
    best_month, revenues = predict_best_release_month(
        ml_data['model'], ml_data['genre_columns'], [selected_genre], selected_budget
    )

    fig = go.Figure(
        go.Scatter(
            x=ml_data['months'],
            y=revenues,
            mode='lines+markers',
            marker=dict(size=8, color='blue'),
            line=dict(color='royalblue'),
            hovertemplate='Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        )
    )

    fig.update_layout(
        title=f"Predicted Revenue for {selected_genre} | ${selected_budget:,}",
        xaxis_title="Month",
        yaxis_title="Predicted Revenue ($)",
        height=300,
        template="plotly_white",
        hovermode='closest'
    )

    return fig