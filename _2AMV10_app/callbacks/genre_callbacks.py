from dash.dependencies import Input, Output, State
from dash import callback_context

def register_genre_callbacks(app, movies):
    @app.callback(
        Output('genre-trends-chart', 'figure'),
        [Input('movie-dropdown', 'value')],
        [State('genre-trends-chart', 'figure')]
    )
    def update_genre_visibility(selected_movie, current_figure):
        if not selected_movie:
            # If no movie is selected, show all genres
            for trace in current_figure['data']:
                trace['visible'] = True
            return current_figure
            
        # Get the selected movie's genres
        movie_row = movies[movies['imdbId'] == selected_movie]
        if movie_row.empty:
            return current_figure
            
        selected_genres = movie_row.iloc[0]['genres'].split('|') if isinstance(movie_row.iloc[0]['genres'], str) else movie_row.iloc[0]['genres']
        
        # Update visibility of traces based on selected movie's genres
        for trace in current_figure['data']:
            trace['visible'] = trace['name'] in selected_genres
            
        return current_figure 