from _2AMV10_app.main import app
from _2AMV10_app.views.menu import make_menu_layout
from _2AMV10_app.views.scatterplot import Scatterplot
from _2AMV10_app.views.movieimage import fetch_movie_image  # Import the function to fetch movie images
from _2AMV10_app.data import get_all_data  # Import the function to get movie data

from dash import html, dcc
from dash.dependencies import Input, Output

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

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                style={"height": "100vh", "padding": "20px"},
                children=[
                    # Search bar for movie title
                    dcc.Input(
                        id="movie-search-bar",
                        type="text",
                        placeholder="Type a movie title...",
                        style={"width": "100%", "marginBottom": "20px"}
                    ),
                    # Div to display the movie poster
                    html.Div(
                        id="movie-poster-container",
                        children="Enter a movie title to see its poster.",
                        style={"textAlign": "center"}
                    )
                ]
            ),
        ]
    )

    # Callback to fetch and display the movie poster
    @app.callback(
        Output("movie-poster-container", "children"),
        [Input("movie-search-bar", "value")]
    )
    def update_movie_poster(movie_title):
        if not movie_title:
            return "Enter a movie title to see its poster."

        # Check if the movie exists in the dataset
        if movie_title not in movies["title"].values:
            return f"Movie '{movie_title}' not found in the dataset."

        # Fetch the movie poster using the API
        poster_url = fetch_movie_image(movie_title)
        if poster_url.startswith("Error"):
            return poster_url  # Return the error message if the API fails

        # Return the image element
        return html.Img(src=poster_url, style={"maxWidth": "100%", "height": "auto"})

    app.run_server(debug=True, dev_tools_ui=False)