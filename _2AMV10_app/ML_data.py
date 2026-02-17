import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import calendar

def load_ml_data():
    # Load the datasets
    df_links = pd.read_csv('data/links.csv')
    df_movies = pd.read_csv('data/movies.csv')
    df_metadata = pd.read_csv('data/movies_metadata.csv')

    # Process metadata
    df_metadata['release_date'] = pd.to_datetime(df_metadata['release_date'], errors='coerce')
    df_metadata = df_metadata.dropna(subset=['genres', 'release_date', 'revenue'])
    df_metadata['release_month'] = df_metadata['release_date'].dt.month
    df_metadata['release_year'] = df_metadata['release_date'].dt.year

    df_release_info = df_metadata[['imdb_id', 'budget', 'release_date', 'release_month', 'release_year', 'revenue']].drop_duplicates()
    df_release_info['imdb_id'] = df_release_info['imdb_id'].str.replace('tt0', '', regex=False)

    # Merge datasets
    df_movies = df_movies.merge(df_links, on='movieId', how='left')
    df_movies = df_movies.rename(columns={'imdbId': 'imdb_id'})

    df_movies['imdb_id'] = df_movies['imdb_id'].astype(str)
    df_release_info['imdb_id'] = df_release_info['imdb_id'].astype(str)

    df_movies = df_movies.merge(df_release_info, on='imdb_id', how='left')
    df_movies = df_movies.dropna()

    # Convert budget to numeric
    df_movies['budget'] = pd.to_numeric(df_movies['budget'], errors='coerce')

    # Create genre one-hot encoded columns
    genre_options = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 
                     'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                     'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    for genre in genre_options:
        df_movies[f'genre_{genre}'] = df_movies['genres'].apply(lambda x: int(genre in x.split('|')))

    # Prepare features for the model
    genre_columns = [f'genre_{genre}' for genre in genre_options]

    df_model = df_movies.dropna(subset=genre_columns + ['budget', 'release_month', 'revenue'])

    X = df_model[genre_columns + ['budget', 'release_month']]
    y = df_model['revenue']

    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    regressor = XGBRegressor(random_state=42)
    regressor.fit(X_train, y_train)

    return {
        'model': regressor,
        'genre_columns': genre_columns,
        'months': list(calendar.month_name[1:]),
        'genre_options': genre_options,
        'budget_options': [20_000_000, 50_000_000, 100_000_000]
    }


def predict_best_release_month(model, genre_columns, genres_list, budget):
    test_rows = []
    
    for month in range(1, 13):
        row = [1 if col.replace("genre_", "") in genres_list else 0 for col in genre_columns]
        row += [budget, month]
        test_rows.append(row)
    
    test_df = pd.DataFrame(test_rows, columns=genre_columns + ['budget', 'release_month'])
    predicted_revenues = model.predict(test_df)
    
    best_month = predicted_revenues.argmax() + 1
    return best_month, predicted_revenues 