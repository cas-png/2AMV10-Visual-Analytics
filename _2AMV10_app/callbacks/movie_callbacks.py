from dash.dependencies import Input, Output
from dash import html
import logging
import pandas as pd
from _2AMV10_app.views.movieimage import fetch_movie_image

# Set up logging
logger = logging.getLogger(__name__)

def register_movie_callbacks(app, movies):
    @app.callback(
        Output("movie-dropdown", "options"),
        [Input("movie-dropdown", "search_value"), Input("movie-dropdown", "value")]
    )
    def update_dropdown_options(search_value, current_value):
        logger.debug(f"Dropdown search triggered with value: {search_value}")

        options = []

        if search_value:
            # Filter movies by search
            filtered_movies = movies[movies["title"].str.contains(search_value, case=False, na=False)].head(10)
            options = [
                {"label": row["title"], "value": row["imdbId"]}
                for _, row in filtered_movies.iterrows()
                if pd.notna(row["imdbId"])
            ]

        # Ensure current selection is preserved
        if current_value and all(opt["value"] != current_value for opt in options):
            # Try to get label from DataFrame
            match = movies[movies["imdbId"] == current_value]
            if not match.empty:
                label = match.iloc[0]["title"]
                options.insert(0, {"label": label, "value": current_value})

        return options

    @app.callback(
        Output("movie-poster-container", "children"),
        [Input("movie-dropdown", "value")]
    )
    def update_movie_poster(imdb_id):
        logger.debug(f"Selected IMDb ID: {imdb_id}")

        if not imdb_id:
            return html.Div("Enter a movie title to see its poster.", 
                            style={"color": "red", "fontSize": "20px"})

        poster_url = fetch_movie_image(imdb_id)
        logger.debug(f"Poster URL: {poster_url}")

        if poster_url.startswith("Error"):
            return html.Div([
                html.H3("Error:", style={"color": "red"}),
                html.P(poster_url)
            ])

        # Get the movie information from the movies DataFrame
        movie_info = movies[movies["imdbId"] == imdb_id].iloc[0]
        movie_title = movie_info["title"]
        genres = movie_info["genres"]
        if isinstance(genres, str):
            genres = genres.split("|")
        avg_rating = round(movie_info["average_rating"], 2)
        rating_count = int(movie_info["rating_count"])

        # Define genre colors
        genre_colors = {
            "Action": "#FF6B6B",
            "Adventure": "#4ECDC4",
            "Animation": "#45B7D1",
            "Children": "#96CEB4",
            "Comedy": "#FFEEAD",
            "Crime": "#D4A5A5",
            "Documentary": "#9B59B6",
            "Drama": "#3498DB",
            "Fantasy": "#F1C40F",
            "Film-Noir": "#34495E",
            "Horror": "#E74C3C",
            "Musical": "#1ABC9C",
            "Mystery": "#7F8C8D",
            "Romance": "#E91E63",
            "Sci-Fi": "#2ECC71",
            "Thriller": "#8E44AD",
            "War": "#C0392B",
            "Western": "#D35400"
        }

        # Create genre tags with colors
        genre_tags = [
            html.Span(
                genre,
                style={
                    "backgroundColor": genre_colors.get(genre, "#95A5A6"),
                    "color": "white",
                    "padding": "4px 8px",
                    "margin": "4px",
                    "borderRadius": "4px",
                    "display": "inline-block",
                    "fontSize": "12px"
                }
            )
            for genre in genres
        ]

        # Create IMDb link
        imdb_link = f"https://www.imdb.com/title/{imdb_id}/"

        return html.Div([
            html.H3(movie_title, style={"marginBottom": "10px"}),
            html.Img(
                src=poster_url,
                style={"maxWidth": "300px", "height": "auto", "border": "2px solid black", "marginBottom": "10px"}
            ),
            html.Div([
                html.Div([
                    html.Span("⭐ ", style={"color": "#FFD700", "fontSize": "20px"}),
                    html.Span(f"{avg_rating}/5.0", style={"fontSize": "16px", "fontWeight": "bold"})
                ], style={"marginBottom": "5px"}),
                html.Div([
                    html.Span("👥 ", style={"fontSize": "16px"}),
                    html.Span(f"{rating_count} ratings", style={"fontSize": "14px"})
                ], style={"marginBottom": "10px"}),
                html.Div(genre_tags, style={"display": "flex", "flexWrap": "wrap", "marginTop": "10px"}),
                html.Div([
                    html.A(
                        "View on IMDb",
                        href=imdb_link,
                        target="_blank",
                        style={
                            "display": "inline-block",
                            "marginTop": "15px",
                            "padding": "8px 16px",
                            "backgroundColor": "#F5C518",
                            "color": "#000000",
                            "textDecoration": "none",
                            "borderRadius": "4px",
                            "fontWeight": "bold"
                        }
                    )
                ], style={"textAlign": "center", "marginTop": "10px"})
            ], style={"textAlign": "center"})
        ], style={"textAlign": "center"}) 