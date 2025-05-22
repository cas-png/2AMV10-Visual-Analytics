from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

def register_chart_callbacks(app, movies, ratings):
    @app.callback(
        Output('selected-chart', 'figure'),
        [Input('chart-selector', 'value'),
         Input('movie-dropdown', 'value')]
    )
    def update_chart(selected_chart, selected_movie):
        # Work on a copy to avoid mutating the original DataFrame
        movies_copy = movies.copy()
        # Only split if genres are strings
        movies_copy['genres'] = movies_copy['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else x)
        movies_exploded = movies_copy.explode('genres')
        
        # Merge with ratings
        movie_ratings = pd.merge(movies_exploded, ratings, on='movieId')
        
        # Get selected movie info if a movie is selected
        selected_movie_info = None
        selected_genres = []
        selected_year = None
        selected_month = None
        if selected_movie:
            movie_row = movies[movies['imdbId'] == selected_movie]
            if not movie_row.empty:
                selected_movie_info = movie_row.iloc[0]
                selected_genres = selected_movie_info['genres'].split('|') if isinstance(selected_movie_info['genres'], str) else selected_movie_info['genres']
                movie_ratings_row = ratings[ratings['movieId'] == selected_movie_info['movieId']]
                if not movie_ratings_row.empty:
                    selected_year = pd.to_datetime(movie_ratings_row['timestamp'].min(), unit='s').year
                    selected_month = pd.to_datetime(movie_ratings_row['timestamp'].min(), unit='s').strftime('%Y-%m')
        
        if selected_chart == 'avg':
            # Calculate average rating per genre
            genre_ratings = movie_ratings.groupby('genres')['rating'].mean().reset_index()
            
            # Highlight selected movie's genres with a color array
            bar_colors = []
            for genre in genre_ratings['genres']:
                if genre in selected_genres:
                    bar_colors.append('#FF0000')  # Red for selected genres
                else:
                    bar_colors.append('#636EFA')  # Default Plotly blue
            
            # Create bar chart for average ratings
            fig = px.bar(
                genre_ratings,
                x='genres',
                y='rating',
                title='Average Rating by Genre',
                labels={'genres': 'Genre', 'rating': 'Average Rating'},
                height=400
            )
            fig.update_traces(marker_color=bar_colors)
            
            # Update layout for better readability
            fig.update_layout(
                xaxis_tickangle=-45,
                xaxis_title="Genre",
                yaxis_title="Average Rating",
                showlegend=False
            )
            
        elif selected_chart == 'counts':
            # Calculate most rated genres
            genre_counts = movie_ratings.groupby('genres').size().reset_index(name='count')
            genre_counts = genre_counts.sort_values('count', ascending=False)
            
            # Highlight selected movie's genres with a color array
            bar_colors = []
            for genre in genre_counts['genres']:
                if genre in selected_genres:
                    bar_colors.append('#FF0000')  # Red for selected genres
                else:
                    bar_colors.append('#636EFA')  # Default Plotly blue
            
            # Create bar chart for most rated genres
            fig = px.bar(
                genre_counts,
                x='genres',
                y='count',
                title='Number of Ratings by Genre',
                labels={'genres': 'Genre', 'count': 'Number of Ratings'},
                height=400
            )
            fig.update_traces(marker_color=bar_colors)
            
            # Update layout for better readability
            fig.update_layout(
                xaxis_tickangle=-45,
                xaxis_title="Genre",
                yaxis_title="Number of Ratings",
                showlegend=False
            )
            
        elif selected_chart == 'years':
            # Convert timestamp to datetime and extract year
            ratings['datetime'] = pd.to_datetime(ratings['timestamp'], unit='s')
            ratings['year'] = ratings['datetime'].dt.year
            yearly_ratings = ratings.groupby('year')['rating'].mean().reset_index()
            
            # Create line chart for ratings by year
            fig = px.line(
                yearly_ratings,
                x='year',
                y='rating',
                title='Average Rating by Year',
                labels={'year': 'Year', 'rating': 'Average Rating'},
                height=400
            )
            
            # Update layout for better readability
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Average Rating",
                showlegend=False,
                hovermode='x unified'
            )
            
            # Update x-axis to show appropriate time format
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=2, label="2y", step="year", stepmode="backward"),
                        dict(count=5, label="5y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            
            # Add vertical line for selected movie's year
            if selected_movie_info is not None and selected_year is not None:
                fig.add_vline(
                    x=selected_year,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Selected Movie ({selected_movie_info['title']})",
                    annotation_position="top right"
                )
            
        else:  # months
            # Convert timestamp to datetime and extract month and year
            ratings['datetime'] = pd.to_datetime(ratings['timestamp'], unit='s')
            ratings['month_year'] = ratings['datetime'].dt.to_period('M').dt.to_timestamp()
            monthly_ratings = ratings.groupby('month_year')['rating'].mean().reset_index()
            
            # Create line chart for ratings by month (x-axis is datetime)
            fig = px.line(
                monthly_ratings,
                x='month_year',
                y='rating',
                title='Average Rating by Month',
                labels={'month_year': 'Month', 'rating': 'Average Rating'},
                height=400
            )
            
            # Update layout for better readability
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Average Rating",
                showlegend=False,
                hovermode='x unified'
            )
            
            # Update x-axis to show appropriate time format
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            
        return fig 