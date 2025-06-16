from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
from ..data import get_all_data

def create_genre_tag_analysis():
    # Load data once
    _, _, _, df_movies, _, df_tags, _ = get_all_data()

    # Processing steps here (as you already have)
    movies_df = df_movies[["movieId", "genres"]].copy()
    movies_df["genres_list"] = movies_df["genres"].str.split("|")
    movie_genres = movies_df.explode("genres_list").rename(columns={"genres_list": "genre"})[["movieId", "genre"]]

    tags_with_genre = df_tags.merge(movie_genres, on="movieId", how="inner")[["movieId", "tag", "genre"]]
    genre_tag_counts = tags_with_genre.drop_duplicates(subset=["movieId", "tag", "genre"]).groupby(["genre", "tag"])["movieId"].nunique().reset_index(name="count_movies_with_tag")
    genre_tag_matrix = genre_tag_counts.pivot(index="genre", columns="tag", values="count_movies_with_tag").fillna(0)

    initial_genre = genre_tag_matrix.index[0]
    top_tags = genre_tag_matrix.loc[initial_genre].sort_values(ascending=False).head(10)

    fig = go.Figure(
        go.Bar(x=top_tags.values, y=top_tags.index, orientation='h')
    )

    fig.update_layout(
        title=f"Top 10 Tags for Genre: {initial_genre}",
        xaxis_title="Count",
        yaxis_title="Tag",
        height=400,
        template="plotly_white"
    )

    return html.Div([
    html.Div([
        html.Label("Select Genre:", className="font-semibold"),
        dcc.Dropdown(
            id='genre-tag-dropdown',
            options=[{'label': genre, 'value': genre} for genre in genre_tag_matrix.index],
            value=initial_genre, style={"marginBottom": "10px"}
        ),
        html.Div(
            dcc.Graph(figure=fig, id='TAG_plot')
        )
    ], className='bg-gray-800 p-4 rounded-lg')
], className='p-4')


@callback(
    Output('TAG_plot', 'figure'),
    Input('genre-tag-dropdown', 'value')
)
def update_tag_plot(selected_genre):
    # Reload data (ideally cached for efficiency)
    _, _, _, df_movies, _, df_tags, _ = get_all_data()

    movies_df = df_movies[["movieId", "genres"]].copy()
    movies_df["genres_list"] = movies_df["genres"].str.split("|")
    movie_genres = movies_df.explode("genres_list").rename(columns={"genres_list": "genre"})[["movieId", "genre"]]

    tags_with_genre = df_tags.merge(movie_genres, on="movieId", how="inner")[["movieId", "tag", "genre"]]
    genre_tag_counts = tags_with_genre.drop_duplicates(subset=["movieId", "tag", "genre"]).groupby(["genre", "tag"])["movieId"].nunique().reset_index(name="count_movies_with_tag")
    genre_tag_matrix = genre_tag_counts.pivot(index="genre", columns="tag", values="count_movies_with_tag").fillna(0)

    top_tags = genre_tag_matrix.loc[selected_genre].sort_values(ascending=False).head(10)

    fig = go.Figure(
        go.Bar(x=top_tags.values, y=top_tags.index, orientation='h')
    )

    fig.update_layout(
        title=f"Top 10 Tags for Genre: {selected_genre}",
        xaxis_title="Count",
        yaxis_title="Tag",
        height=300,
        template="plotly_white"
    )

    return fig
