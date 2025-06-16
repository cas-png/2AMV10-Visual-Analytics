from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from ..data import get_all_data

def create_genre_tag_analysis():
    # Load data once - keeping your exact processing logic but adding TF-IDF
    _, _, _, df_movies, _, df_tags, _ = get_all_data()

    # Your original processing steps
    movies_df = df_movies[["movieId", "genres"]].copy()
    movies_df["genres_list"] = movies_df["genres"].str.split("|")
    movie_genres = movies_df.explode("genres_list").rename(columns={"genres_list": "genre"})[["movieId", "genre"]]

    tags_with_genre = df_tags.merge(movie_genres, on="movieId", how="inner")[["movieId", "tag", "genre"]]
    genre_tag_counts = tags_with_genre.drop_duplicates(subset=["movieId", "tag", "genre"]).groupby(["genre", "tag"])["movieId"].nunique().reset_index(name="count_movies_with_tag")
    genre_tag_matrix = genre_tag_counts.pivot(index="genre", columns="tag", values="count_movies_with_tag").fillna(0)

    return html.Div([
        html.Div([
            html.Label("Select Genre:", className="font-semibold"),
            dcc.Dropdown(
                id='genre-tag-dropdown',
                options=[{'label': genre, 'value': genre} for genre in genre_tag_matrix.index],
                value=genre_tag_matrix.index[0], 
                style={"marginBottom": "10px"}
            ),
            dcc.Graph(id='TAG_plot', style={'height': '325x'})
        ], className='bg-gray-800 p-4 rounded-lg')
    ], className='p-4')

@callback(
    Output('TAG_plot', 'figure'),
    Input('genre-tag-dropdown', 'value')
)
def update_tag_plot(selected_genre):
    # Reload data (ideally cached for efficiency)
    _, _, _, df_movies, _, df_tags, _ = get_all_data()

    # Same processing as before
    movies_df = df_movies[["movieId", "genres"]].copy()
    movies_df["genres_list"] = movies_df["genres"].str.split("|")
    movie_genres = movies_df.explode("genres_list").rename(columns={"genres_list": "genre"})[["movieId", "genre"]]

    tags_with_genre = df_tags.merge(movie_genres, on="movieId", how="inner")[["movieId", "tag", "genre"]]
    genre_tag_counts = tags_with_genre.drop_duplicates(subset=["movieId", "tag", "genre"]).groupby(["genre", "tag"])["movieId"].nunique().reset_index(name="count_movies_with_tag")
    genre_tag_matrix = genre_tag_counts.pivot(index="genre", columns="tag", values="count_movies_with_tag").fillna(0)

    tfidf = TfidfTransformer(norm="l2", smooth_idf=True)
    tfidf_matrix = tfidf.fit_transform(genre_tag_matrix.values)
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        index=genre_tag_matrix.index,    
        columns=genre_tag_matrix.columns  
    )

    # Get top tags using TF-IDF scores instead of counts
    top_tags_tfidf = tfidf_df.loc[selected_genre].sort_values(ascending=False).head(10)

    # Create the figure using TF-IDF scores
    fig = go.Figure(
        go.Bar(x=top_tags_tfidf.values, y=top_tags_tfidf.index, orientation='h')
    )

    fig.update_layout(
        title=f"Top 10 Tags for Genre: {selected_genre}",
        xaxis_title="TF-IDF Score",  # Changed from "Count" to "TF-IDF Score"
        yaxis_title="Tag",
        height=325,
        template="plotly_white"
    )
    
    return fig