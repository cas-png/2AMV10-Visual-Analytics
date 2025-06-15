from dash import html, dcc
from .scatter_plot import create_genre_ratings_chart
from .genre_trends import create_genre_trends_chart
from .top_rated_movies import create_top_rated_movies_chart
from .machine_learning import create_machine_learning_layout

def create_movie_layout(movies, ratings, genre):
    return html.Div(
        id="app-container",
        style={"height": "100vh", "display": "flex", "flexDirection": "row"},
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                style={"height": "100vh", "overflowY": "auto"},
                children=[
                    dcc.Dropdown(
                        id="movie-dropdown",
                        options=[],
                        placeholder="Type a movie title...",
                        style={"width": "100%", "marginBottom": "10px"},
                        searchable=True,
                    ),
                    html.Div(
                        id="movie-poster-container",
                        style={"textAlign": "center", "marginTop": "10px", "maxWidth": "100%"},
                    ),
                ]
            ),

            html.Div(
                id="right-column",
                className="nine columns",
                style={"height": "100vh", "padding": "20px", "overflowY": "auto"},
                children=[
                    dcc.Tabs(
                        id="tab-selector",
                        value="overview",
                        style={"padding-bottom": "10px", "fontWeight": "bold"},
                        children=[
                            dcc.Tab(
                                label="Movie Analytics Dashboard",
                                value="overview",
                                children=[
                                    create_genre_ratings_chart(movies, ratings),
                                    create_genre_trends_chart(genre)
                                ]
                            ),
                            dcc.Tab(
                                label="General Insights",
                                value="insights",
                                children=[
                                    create_top_rated_movies_chart(movies)
                                ]
                            ),
                            dcc.Tab(
                                label="Machine Learning",
                                value="machine_learning",
                                children=[
                                    create_machine_learning_layout()
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    ) 