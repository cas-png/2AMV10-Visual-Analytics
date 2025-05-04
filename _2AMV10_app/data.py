import pandas as pd
from pathlib import Path

def get_all_data():
    # Define the path to the ml-latest folder
    ml_latest_path = Path(__file__).resolve().parent.parent.parent / "ml-latest"
    if not ml_latest_path.exists():
        raise FileNotFoundError(f"Folder not found at {ml_latest_path}")

    # Load all CSV files
    genome_scores = pd.read_csv(ml_latest_path / "genome-scores.csv")
    genome_tags = pd.read_csv(ml_latest_path / "genome-tags.csv")
    links = pd.read_csv(ml_latest_path / "links.csv")
    movies = pd.read_csv(ml_latest_path / "movies.csv")
    ratings = pd.read_csv(ml_latest_path / "ratings.csv")
    tags = pd.read_csv(ml_latest_path / "tags.csv")

    # Add formatted IMDb IDs to links
    links["imdbId"] = links["imdbId"].apply(lambda x: f"tt{int(x):07d}")

    # Merge imdbId into movies
    movies = movies.merge(links[["movieId", "imdbId"]], on="movieId", how="left")

    return genome_scores, genome_tags, links, movies, ratings, tags

if __name__ == "__main__":
    genome_scores, genome_tags, links, movies, ratings, tags = get_all_data()
    

    print(movies[movies["imdbId"] == 'tt0111161'])
    
    
