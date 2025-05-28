#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools
import numpy as np
from math import factorial
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample
import pandas as pd
import geopandas as gpd
import requests
from datetime import datetime


# In[2]:


df_links = pd.read_csv('C:/data/links.csv')
df_movies = pd.read_csv('C:/data/movies.csv')
df_ratings = pd.read_csv('C:/data/ratings.csv')
df_tags = pd.read_csv('C:/data/tags.csv')
df_metadata = pd.read_csv('C:/data/movies_metadata.csv')


df_movies


# In[3]:


df_metadata['release_date'] = pd.to_datetime(df_metadata['release_date'], errors='coerce')
df_metadata = df_metadata.dropna(subset=['genres', 'release_date', 'revenue'])
df_metadata['release_month'] = df_metadata['release_date'].dt.month
df_metadata['release_year'] = df_metadata['release_date'].dt.year

df_release_info = df_metadata[['imdb_id', 'budget', 'release_date', 'release_month', 'release_year', 'revenue']].drop_duplicates()
df_release_info['imdb_id'] = df_release_info['imdb_id'].str.replace('tt0', '', regex=False)


# In[4]:


df_release_info


# In[5]:


df_movies = df_movies.merge(df_links, on='movieId', how='left')
df_movies = df_movies.rename(columns={'imdbId': 'imdb_id'})

df_movies['imdb_id'] = df_movies['imdb_id'].astype(str)
df_release_info['imdb_id'] = df_release_info['imdb_id'].astype(str)

df_movies = df_movies.merge(df_release_info, on='imdb_id', how='left')
df_movies = df_movies.dropna()

for col in ['budget']:
    df_movies[col] = pd.to_numeric(df_movies[col], errors='coerce')
    


# In[6]:


df_movies


# In[7]:


genre_columns = [col for col in df_movies.columns if col.startswith("genre_")]
genre_columns = [col for col in genre_columns if col != 'genre_signature']

df_model = df_movies.dropna(subset=genre_columns + ['budget', 'release_month', 'revenue'])

df_model['budget'] = pd.to_numeric(df_model['budget'], errors='coerce')

X = df_model[genre_columns + ['budget', 'release_month']]
y = df_model['revenue']


# In[8]:


from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

regressor = XGBRegressor(random_state=42)
regressor.fit(X_train, y_train)


# In[9]:


def predict_best_release_month(genres_list, budget):
    test_rows = []
    
    for month in range(1, 13):
        row = [1 if col.replace("genre_", "") in genres_list else 0 for col in genre_columns]
        
        row += [budget, month]
        test_rows.append(row)
    
    test_df = pd.DataFrame(test_rows, columns=genre_columns + ['budget', 'release_month'])
    
    predicted_revenues = regressor.predict(test_df)
    
    best_month = predicted_revenues.argmax() + 1
    return best_month, predicted_revenues


# In[10]:


best_month, predicted_revenues = predict_best_release_month(['Romance'], budget=333333)
print(f"Best month to release: {best_month}")
print("Predicted revenue per month:", predicted_revenues)


# In[11]:


test_cases = [
    (['Comedy'], 5e6),
    (['Drama'], 1e7),
    (['Action'], 5e7),
    (['Action', 'Sci-Fi'], 1e8),
    (['Romance'], 3e6),
    (['Horror'], 2e6),
    (['Animation'], 7e7),
]

for genres, budget in test_cases:
    best_month, predicted_revenues = predict_best_release_month(genres, budget)
    print(f"{genres} | Budget: ${budget:,.0f} → Best month: {best_month}")
    print("Revenues:", [f"{rev:,.0f}" for rev in predicted_revenues])
    print("-" * 60)


# In[12]:


import plotly.graph_objs as go
import calendar

months = list(calendar.month_name[1:]) 

fig = go.Figure(data=go.Scatter(
    x=months,
    y=predicted_revenues,
    mode='lines+markers',
    marker=dict(size=8, color='blue'),
    line=dict(color='royalblue'),
    hoverinfo='x+y',
))

fig.update_layout(
    title='📈 Predicted Revenue by Release Month',
    xaxis_title='Month',
    yaxis_title='Predicted Revenue ($)',
    hovermode='closest',
    template='plotly_white'
)

fig.show()


# In[14]:


import plotly.graph_objects as go
import calendar
import itertools
import numpy as np

genre_options = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Romance']
budget_options = [20_000_000, 50_000_000, 100_000_000]

predictions = {}

for genre, budget in itertools.product(genre_options, budget_options):
    best_month, revenues = predict_best_release_month([genre], budget)
    predictions[(genre, budget)] = revenues

months = list(calendar.month_name[1:])
initial_genre = genre_options[0]
initial_budget = budget_options[0]
initial_data = predictions[(initial_genre, initial_budget)]

fig = go.Figure()

trace = go.Scatter(
    x=months,
    y=initial_data,
    mode='lines+markers',
    name=f"{initial_genre} | ${initial_budget:,}",
    hovertemplate='Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
)
fig.add_trace(trace)

genre_buttons = []
for genre in genre_options:
    visible = [True]
    trace_name = f"{genre} | ${initial_budget:,}"
    new_y = predictions[(genre, initial_budget)]
    genre_buttons.append(dict(
        label=genre,
        method='update',
        args=[
            {'y': [new_y]},
            {'title': f'Predicted Revenue for {genre} | ${initial_budget:,}'}
        ]
    ))

budget_buttons = []
for budget in budget_options:
    visible = [True]
    trace_name = f"{initial_genre} | ${budget:,}"
    new_y = predictions[(initial_genre, budget)]
    budget_buttons.append(dict(
        label=f"${budget//1_000_000}M",
        method='update',
        args=[
            {'y': [new_y]},
            {'title': f'Predicted Revenue for {initial_genre} | ${budget:,}'}
        ]
    ))

fig.update_layout(
    title=f"Predicted Revenue for {initial_genre} | ${initial_budget:,}",
    xaxis_title="Month",
    yaxis_title="Predicted Revenue ($)",
    updatemenus=[
        dict(
            buttons=genre_buttons,
            direction="down",
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.2,
            yanchor="top",
            pad={"r": 10, "t": 10},
            name="genre"
        ),
        dict(
            buttons=budget_buttons,
            direction="down",
            showactive=True,
            x=0.35,
            xanchor="left",
            y=1.2,
            yanchor="top",
            pad={"r": 10, "t": 10},
            name="budget"
        ),
    ],
    height=700,
    template="plotly_white"
)

fig.show()

