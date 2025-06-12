from dash.dependencies import Input, Output, State
from dash import html, callback_context
import math

def register_top_rated_callbacks(app, movies):
    @app.callback(
        [Output('top-rated-movies-list', 'children'),
         Output('page-indicator', 'children')],
        [Input('prev-page-btn', 'n_clicks'),
         Input('next-page-btn', 'n_clicks'),
         Input('min-ratings-input', 'value'),
         Input('rating-range-slider', 'value')],
        [State('page-indicator', 'children')]
    )
    def update_top_movies(prev_clicks, next_clicks, min_ratings, rating_range, page_indicator):
        # Determine current page
        page_size = 10
        trigger = callback_context.triggered[0]['prop_id'].split('.')[0]
        # Extract current page from indicator, fallback to 1
        if page_indicator and isinstance(page_indicator, str) and '/' in page_indicator:
            try:
                current_page = int(page_indicator.split()[1])
            except Exception:
                current_page = 1
        else:
            current_page = 1
        # Update page based on button clicks
        if trigger == 'next-page-btn':
            current_page += 1
        elif trigger == 'prev-page-btn':
            current_page -= 1
        # Never go below page 1
        if current_page < 1:
            current_page = 1
        # Filter movies based on minimum ratings and rating range
        filtered_movies = movies[
            (movies['rating_count'] >= min_ratings) &
            (movies['average_rating'] >= rating_range[0]) &
            (movies['average_rating'] <= rating_range[1])
        ]
        total_movies = len(filtered_movies)
        total_pages = max(1, math.ceil(total_movies / page_size))
        # Never go above max page
        if current_page > total_pages:
            current_page = total_pages
        # Calculate the start and end indices for the selected page
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        # Sort filtered movies by average rating and get the selected page
        top_movies = filtered_movies.sort_values('average_rating', ascending=False).iloc[start_idx:end_idx]
        row_style = {
            "display": "flex",
            "alignItems": "center",
            "padding": "0 0",
            "borderBottom": "1px solid #eee",
            "minHeight": "48px",
            "maxHeight": "48px",
            "height": "48px"
        }
        # Header row
        header = html.Div([
            html.Div("#", style={"width": "40px", "fontWeight": "bold", "color": "#2c8cff", "textAlign": "right"}),
            html.Div("Title", style={"flex": "2", "fontWeight": "bold", "paddingLeft": "10px"}),
            html.Div("Genres", style={"flex": "2", "fontWeight": "bold", "color": "#666", "paddingLeft": "10px"}),
            html.Div("Rating / Users", style={"width": "120px", "fontWeight": "bold", "textAlign": "right", "color": "#666"})
        ], style={
            **row_style,
            "borderBottom": "2px solid #bbb",
            "background": "#f7f7f7"
        })
        # Create a list of movie items
        movie_list = [header]
        for i, (_, movie) in enumerate(top_movies.iterrows()):
            genres = movie['genres']
            if isinstance(genres, (list, tuple)):
                genres_str = f"[{', '.join(genres)}]"
            elif isinstance(genres, str):
                genres_str = f"[{', '.join(eval(genres) if genres.startswith('[') else genres.split('|'))}]"
            else:
                genres_str = "[]"
            movie_list.append(
                html.Div([
                    html.Div(f"{start_idx + i + 1}.", style={"width": "40px", "fontWeight": "bold", "color": "#2c8cff", "textAlign": "right"}),
                    html.Div(movie['title'], style={"flex": "2", "fontWeight": "bold", "paddingLeft": "10px"}),
                    html.Div(genres_str, style={"flex": "2", "color": "#666", "paddingLeft": "10px"}),
                    html.Div([
                        html.Span(f"⭐ {movie['average_rating']:.2f}", style={"color": "#FFD700", "marginRight": "10px"}),
                        html.Span(f"👥 {movie['rating_count']}", style={"color": "#666"})
                    ], style={"width": "120px", "textAlign": "right"})
                ], style=row_style)
            )
        # If no movies match the criteria
        if len(movie_list) == 1:
            return html.Div(
                "No movies match the selected criteria. Try adjusting the filters.",
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "color": "#666"
                }
            ), f"Page {current_page} / {total_pages}"
        return movie_list, f"Page {current_page} / {total_pages}" 