from dash import Input, Output, State
import plotly.graph_objects as go
import calendar
import pandas as pd
from xgboost import XGBRegressor

def prepare_model_data(movies_metadata):
    # Prepare data for XGBoost
    df_metadata = movies_metadata.copy()
    df_metadata['release_date'] = pd.to_datetime(df_metadata['release_date'], errors='coerce')
    df_metadata = df_metadata.dropna(subset=['genres', 'release_date', 'revenue'])
    df_metadata['release_month'] = df_metadata['release_date'].dt.month
    
    # Create genre columns
    all_genres = set()
    for genres in df_metadata['genres']:
        if isinstance(genres, str):
            genre_list = eval(genres)
            all_genres.update([g['name'] for g in genre_list])
    
    for genre in all_genres:
        df_metadata[f'genre_{genre}'] = df_metadata['genres'].apply(
            lambda x: 1 if isinstance(x, str) and any(g['name'] == genre for g in eval(x)) else 0
        )
    
    genre_columns = [col for col in df_metadata.columns if col.startswith("genre_")]
    
    # Prepare model data
    df_model = df_metadata.dropna(subset=genre_columns + ['budget', 'release_month', 'revenue'])
    df_model['budget'] = pd.to_numeric(df_model['budget'], errors='coerce')
    
    X = df_model[genre_columns + ['budget', 'release_month']]
    y = df_model['revenue']
    
    # Train model
    regressor = XGBRegressor(random_state=42)
    regressor.fit(X, y)
    
    return regressor, genre_columns

def register_xgboost_callbacks(app, movies_metadata):
    # Train model once and store it
    regressor, genre_columns = prepare_model_data(movies_metadata)
    
    @app.callback(
        Output('revenue-prediction-graph', 'figure'),
        [Input('genre-dropdown', 'value'),
         Input('budget-dropdown', 'value')]
    )
    def update_graph(selected_genre, selected_budget):
        if selected_genre is None or selected_budget is None:
            return go.Figure()
            
        def predict_best_release_month(genres_list, budget):
            test_rows = []
            for month in range(1, 13):
                row = [1 if col.replace("genre_", "") in genres_list else 0 for col in genre_columns]
                row += [budget, month]
                test_rows.append(row)
            
            test_df = pd.DataFrame(test_rows, columns=genre_columns + ['budget', 'release_month'])
            predicted_revenues = regressor.predict(test_df)
            return predicted_revenues
        
        # Get predictions for selected genre and budget
        predicted_revenues = predict_best_release_month([selected_genre], selected_budget)
        
        # Create figure
        months = list(calendar.month_name[1:])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=predicted_revenues,
            mode='lines+markers',
            name=f"{selected_genre} | ${selected_budget:,}",
            hovertemplate='Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Predicted Revenue for {selected_genre} | ${selected_budget:,}",
            xaxis_title="Month",
            yaxis_title="Predicted Revenue ($)",
            height=700,
            template="plotly_white"
        )
        
        return fig 