import pandas as pd
from pathlib import Path

def get_all_data():
    # Get the base directory (project root)
    data_dir = Path(__file__).resolve().parent.parent / "data"

    # Build paths to the CSV files in the data folder
    genome_scores = pd.DataFrame()  # Set as empty DataFrame
    genome_tags = pd.read_csv(data_dir / "genome-tags.csv")
    links = pd.read_csv(data_dir / "links.csv")
    movies = pd.read_csv(data_dir / "movies.csv")
    ratings = pd.read_csv(data_dir / "ratings.csv")
    tags = pd.read_csv(data_dir / "tags.csv")

    # Add formatted IMDb IDs to links
    links["imdbId"] = links["imdbId"].apply(lambda x: f"tt{int(x):07d}")

    # Calculate average rating and rating count for each movie
    movie_ratings = ratings.groupby('movieId').agg({
        'rating': ['mean', 'count']
    }).reset_index()
    movie_ratings.columns = ['movieId', 'average_rating', 'rating_count']

    # Merge imdbId into movies
    movies = movies.merge(links[["movieId", "imdbId"]], on="movieId", how="left")
    
    # Merge rating statistics into movies
    movies = movies.merge(movie_ratings, on="movieId", how="left")
    
    # Fill NaN values for movies with no ratings
    movies['average_rating'] = movies['average_rating'].fillna(0)
    movies['rating_count'] = movies['rating_count'].fillna(0)

    def get_genre_data(movies, ratings):
        """
        Creates a DataFrame with average rating per genre per year,
        based on the earliest rating timestamp per movie.
        """
        # Step 1: Copy movies DataFrame
        genre = movies.copy()

        # Step 2: Merge in ratings to get earliest rating year
        first_ratings = (
            ratings.groupby('movieId')['timestamp']
            .min()
            .reset_index()
        )
        first_ratings['year'] = pd.to_datetime(first_ratings['timestamp'], unit='s').dt.year

        # Step 3: Merge year into genre DataFrame
        genre = genre.merge(first_ratings[['movieId', 'year']], on='movieId', how='left')

        # Step 4: Split and explode genres
        genre['genres'] = genre['genres'].str.split('|')
        genre = genre.explode('genres')

        # Step 5: Group by year and genre
        genre = (
            genre.groupby(['year', 'genres'])['average_rating']
            .mean()
            .reset_index()
            .rename(columns={'genres': 'genre', 'average_rating': 'avg_rating'})
        )

        return genre

    genre = get_genre_data(movies, ratings)
    return genome_scores, genome_tags, links, movies, ratings, tags, genre

if __name__ == "__main__":
    genome_scores, genome_tags, links, movies, ratings, tags, genre = get_all_data()
    
    # Print example movie with its rating statistics
    print(movies[movies["imdbId"] == 'tt0111161'])
    print(genre)
    print(ratings)

    # Convert the timestamp to datetime
    ratings['datetime'] = pd.to_datetime(ratings['timestamp'], unit='s')

    ratings.sort_values(by="datetime", ascending=True)
    print(ratings)
    print(movies)