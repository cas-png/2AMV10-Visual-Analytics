from _2AMV10_app.main import app
from _2AMV10_app.views.menu import make_menu_layout
from _2AMV10_app.views.scatterplot import Scatterplot
from _2AMV10_app.views.movieimage import fetch_movie_image  # Import the function to fetch movie images
from _2AMV10_app.data import get_all_data  # Import the function to get movie data

from dash import html, dcc
from dash.dependencies import Input, Output
import logging
import pandas as pd

# 🔧 Set up logging BEFORE any function uses `logger`
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load the movies DataFrame
_, _, _, movies, _, _ = get_all_data()

if __name__ == '__main__':
    app.layout = html.Div(
        id="app-container",
        style={"height": "100vh", "display": "flex", "flexDirection": "row"},  # Full viewport height
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                style={"height": "100vh", "overflowY": "auto"},  # Scrollable if needed
                children=make_menu_layout()
            ),

            html.Div(
                id="right-column",
                className="nine columns",
                style={"height": "100vh", "padding": "20px", "display": "flex", "flexDirection": "column", "alignItems": "center"},
                children=[
                    dcc.Dropdown(
                        id="movie-dropdown",
                        options=[],
                        placeholder="Type a movie title...",
                        style={"width": "100%", "marginBottom": "20px"},
                        searchable=True,
                    ),
                    html.Div(
                        id="movie-poster-container",
                        style={"textAlign": "center", "marginTop": "10px", "maxWidth": "100%"},
                    ),
                ]
            )
        ]
    )

    @app.callback(
        Output("movie-dropdown", "options"),
        [Input("movie-dropdown", "search_value")]
    )
    def update_dropdown_options(search_value):
        if not search_value:
            return []

        # Filter movies by search
        filtered_movies = movies[movies["title"].str.contains(search_value, case=False, na=False)]

        # Limit to 10 results
        filtered_movies = filtered_movies.head(10)

        # Show full title, pass IMDb ID as value
        return [
            {"label": row["title"], "value": row["imdbId"]}
            for _, row in filtered_movies.iterrows()
            if pd.notna(row["imdbId"])  # skip if imdbId is missing
        ]

    @app.callback(
    Output("movie-poster-container", "children"),
    [Input("movie-dropdown", "value")]
    )
    def update_movie_poster(movie_title):
        logger.debug("Callback triggered.")
        logger.debug(f"Selected title: {movie_title}")

        if not movie_title:
            logger.debug("No title selected.")
            return "Enter a movie title to see its poster."

        poster_url = fetch_movie_image(movie_title)
        logger.debug(f"Fetched poster URL: {poster_url}")

        if poster_url.startswith("Error"):
            logger.warning("Poster fetch failed. Showing fallback.")
            return html.Div([
                html.P("Poster not found or error occurred."),
                html.P(poster_url),
                html.Img(src="/assets/fallback-image.jpg", style={"maxWidth": "100%", "height": "auto"})
            ])

        logger.info("Poster found. Displaying image.")
        return html.Img(src=poster_url, style={"maxWidth": "100%", "height": "auto"})

    app.run_server(debug=True, dev_tools_ui=True)
