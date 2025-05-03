import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_movie_image(title):
    """
    Fetches the poster image URL for a given movie title using the OMDb API.

    Args:
        title (str): The title of the movie.

    Returns:
        str: The URL of the movie poster, or a message if not found.
    """
    # Get the API key from the environment variable
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        raise ValueError("OMDB_API_KEY not found in environment variables")

    # Base URL for the OMDb API
    base_url = "http://www.omdbapi.com/"

    # Parameters for the API request
    params = {
        "i": title,  # Movie title
        "apikey": api_key,  # Your API key
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            # Return the poster URL
            return data.get("Poster", "No poster available")
        else:
            # Return the error message from the API
            return f"Error: {data.get('Error', 'Movie not found')}"
    else:
        return f"Error: Unable to fetch data (status code: {response.status_code})"

# Test the function
if __name__ == "__main__":
    movie_title = "Inception"
    poster_url = fetch_movie_image(movie_title)
    print(f"Poster URL for '{movie_title}': {poster_url}")