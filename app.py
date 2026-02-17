from _2AMV10_app.main import app
from _2AMV10_app.data import get_all_data
from _2AMV10_app.views.movie_layout import create_movie_layout
from _2AMV10_app.callbacks.movie_callbacks import register_movie_callbacks
from _2AMV10_app.callbacks.chart_callbacks import register_chart_callbacks
from _2AMV10_app.callbacks.genre_callbacks import register_genre_callbacks
from _2AMV10_app.callbacks.top_rated_callbacks import register_top_rated_callbacks
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Load the movies DataFrame
    _, _, _, movies, ratings, _, genre = get_all_data()
    
    # Set up the layout
    app.layout = create_movie_layout(movies, ratings, genre)
    
    # Register callbacks
    register_movie_callbacks(app, movies, ratings)
    register_chart_callbacks(app, movies, ratings)
    register_genre_callbacks(app, movies)
    register_top_rated_callbacks(app, movies)
    
    # Run the app
    app.run(debug=True, dev_tools_ui=True)
