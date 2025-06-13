from dash import html, dcc
import plotly.express as px
import pandas as pd
from datetime import datetime

def create_genre_ratings_chart(movies, ratings):
    # Split genres and create a row for each genre
    movies['genres'] = movies['genres'].str.split('|')
    movies_exploded = movies.explode('genres')
    
    # Merge with ratings
    movie_ratings = pd.merge(movies_exploded, ratings, on='movieId')
    
    # Calculate average rating per genre
    genre_ratings = movie_ratings.groupby('genres')['rating'].mean().reset_index()
    
    # Create bar chart for average ratings
    fig_avg = px.bar(
        genre_ratings,
        x='genres',
        y='rating',
        title='Average Rating by Genre',
        labels={'genres': 'Genre', 'rating': 'Average Rating'},
        height=300
    )
    
    # Update layout for better readability
    fig_avg.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Genre",
        yaxis_title="Average Rating",
        showlegend=False
    )
    
    # Calculate most rated genres
    genre_counts = movie_ratings.groupby('genres').size().reset_index(name='count')
    genre_counts = genre_counts.sort_values('count', ascending=False)
    
    # Create bar chart for most rated genres
    fig_counts = px.bar(
        genre_counts,
        x='genres',
        y='count',
        title='Number of Ratings by Genre',
        labels={'genres': 'Genre', 'count': 'Number of Ratings'},
        height=300
    )
    
    # Update layout for better readability
    fig_counts.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Genre",
        yaxis_title="Number of Ratings",
        showlegend=False
    )
    
    # Extract year from timestamp and create year distribution chart
    ratings['year'] = pd.to_datetime(ratings['timestamp'], unit='s').dt.year
    year_ratings = ratings.groupby('year')['rating'].mean().reset_index()
    
    # Create line chart for ratings by year
    fig_years = px.line(
        year_ratings,
        x='year',
        y='rating',
        title='Average Rating by Year',
        labels={'year': 'Year', 'rating': 'Average Rating'},
        height=300
    )
    
    # Update layout for better readability
    fig_years.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Rating",
        showlegend=False
    )
    
    return html.Div([
        dcc.Dropdown(
            id='chart-selector',
            options=[
                {'label': 'Average Rating by Genre', 'value': 'avg'},
                {'label': 'Most Rated Genres', 'value': 'counts'},
                {'label': 'Ratings by Year', 'value': 'years'},
                {'label': 'Ratings by Month', 'value': 'months'}
            ],
            value='avg',
            style={'width': '50%', 'marginBottom': '10px'}
        ),
        dcc.Graph(id='selected-chart', style={'height': '400px'})
    ]) 