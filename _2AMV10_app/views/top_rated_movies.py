from dash import html, dcc
import plotly.express as px
import pandas as pd

def create_top_rated_movies_chart(movies):
    # Sort movies by average rating and get top 10
    top_movies = movies.sort_values('average_rating', ascending=False).head(10)
    
    # Create a list of movie items (dummy for initial render)
    movie_list = []
    for i, (_, movie) in enumerate(top_movies.iterrows()):
        # Format genres as [Action, Comedy]
        genres = movie['genres']
        if isinstance(genres, (list, tuple)):
            genres_str = f"[{', '.join(genres)}]"
        elif isinstance(genres, str):
            genres_str = f"[{', '.join(eval(genres) if genres.startswith('[') else genres.split('|'))}]"
        else:
            genres_str = "[]"
        movie_list.append(
            html.Div([
                html.Div([
                    html.Div(f"{i+1}.", style={"width": "40px", "fontWeight": "bold", "color": "#2c8cff", "textAlign": "right"}),
                    html.Div(movie['title'], style={"flex": "2", "fontWeight": "bold", "paddingLeft": "10px"}),
                    html.Div(genres_str, style={"flex": "2", "color": "#666", "paddingLeft": "10px"}),
                    html.Div([
                        html.Span(f"⭐ {movie['average_rating']:.2f}", style={"color": "#FFD700", "marginRight": "10px"}),
                        html.Span(f"👥 {movie['rating_count']}", style={"color": "#666"})
                    ], style={"width": "120px", "textAlign": "right"})
                ], style={
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "10px 0",
                    "borderBottom": "1px solid #eee"
                })
            ])
        )
    
    return html.Div([
        html.H2("Top Rated Movies", style={"marginBottom": "10px", "fontWeight": "bold", "placement": "center"}),
        
        # Filters container
        html.Div([
            # Minimum ratings filter
            html.Div([
                html.Label("Minimum number of ratings:", style={"marginRight": "10px"}),
                dcc.Input(
                    id='min-ratings-input',
                    type='number',
                    value=100,
                    min=0,
                    style={
                        "width": "100px",
                        "padding": "5px",
                        "borderRadius": "4px",
                        "border": "1px solid #ccc"
                    }
                )
            ], style={"marginBottom": "15px"}),
            
            # Rating range slider
            html.Div([
                html.Label("Rating range:", style={"marginRight": "10px"}),
                dcc.RangeSlider(
                    id='rating-range-slider',
                    min=0,
                    max=5,
                    step=0.1,
                    value=[0, 5],
                    marks={i: f'{i}' for i in range(6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={"marginBottom": "15px"}),
            
            # Pagination controls
            html.Div([
                html.Button('Previous Page', id='prev-page-btn', n_clicks=0, style={"marginRight": "10px"}),
                html.Span(id='page-indicator', style={"fontWeight": "bold", "marginRight": "10px"}),
                html.Button('Next Page', id='next-page-btn', n_clicks=0)
            ], style={"marginBottom": "0px", "marginTop": "10px"})
        ], style={
            "backgroundColor": "white",
            "padding": "15px",
            "borderRadius": "1rem",
            "marginBottom": "20px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
        }),
        
        # Movies list
        html.Div(
            id='top-rated-movies-list',
            style={
                "backgroundColor": "white",
                "borderRadius": "1rem",
                "padding": "1rem",
                "marginTop": "10px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
            },
            children=movie_list
        )
    ]) 