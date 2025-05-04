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

        poster_url = fetch_movie_image(imdb_id)  # this must be fixed as above
        logger.debug(f"Poster URL: {poster_url}")

        if poster_url.startswith("Error"):
            return html.Div([
                html.H3("Error:", style={"color": "red"}),
                html.P(poster_url)
            ])

        return html.Div([
            html.H3(f"IMDb ID: {imdb_id}"),
            html.Img(
                src=poster_url,
                style={"maxWidth": "300px", "height": "auto", "border": "2px solid black"}
            )
        ])


    app.run_server(debug=True, dev_tools_ui=True)
