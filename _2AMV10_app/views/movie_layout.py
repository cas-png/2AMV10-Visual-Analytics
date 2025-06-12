from dash import html, dcc
from .scatter_plot import create_genre_ratings_chart
from .genre_trends import create_genre_trends_chart

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
                                    #create_general_insights(movies)
                                ]
                            ),
                            dcc.Tab(
                                label="Machine Learning",
                                value="machine_learning",
                                children=[
                                    html.Div(
                                        "Machine Learning content will be added here soon.",
                                        style={"textAlign": "center", "marginTop": "20px"}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )

        ]
    ) 