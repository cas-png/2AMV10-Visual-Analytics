from dash import html, dcc
import plotly.express as px
import pandas as pd

def create_genre_trends_chart(genre_df):
    # Define genre colors
    genre_colors = {
        "Action": "#FF6B6B",
        "Adventure": "#4ECDC4",
        "Animation": "#45B7D1",
        "Children": "#96CEB4",
        "Comedy": "#FFEEAD",
        "Crime": "#D4A5A5",
        "Documentary": "#9B59B6",
        "Drama": "#3498DB",
        "Fantasy": "#F1C40F",
        "Film-Noir": "#34495E",
        "Horror": "#E74C3C",
        "Musical": "#1ABC9C",
        "Mystery": "#7F8C8D",
        "Romance": "#E91E63",
        "Sci-Fi": "#2ECC71",
        "Thriller": "#8E44AD",
        "War": "#C0392B",
        "Western": "#D35400"
    }
    
    # Filter out non-genre entries
    genre_df = genre_df[genre_df['genre'].isin(genre_colors.keys())]
    
    # Create the line chart
    fig = px.line(
        genre_df,
        x='year',
        y='avg_rating',
        color='genre',
        title='Average Rating by Genre Over Time',
        labels={
            'year': 'Year',
            'avg_rating': 'Average Rating',
            'genre': 'Genre'
        },
        height=400,
        color_discrete_map=genre_colors
    )
    
    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Rating",
        hovermode='x unified',
        legend_title="Genres",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        )
    )
    
    # Add range slider
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=10, label="10y", step="year", stepmode="backward"),
                dict(count=20, label="20y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    return html.Div([
        html.H2(),
        dcc.Graph(
            id='genre-trends-chart',
            figure=fig,
            style={'height': '40vh'}
        )
    ]) 