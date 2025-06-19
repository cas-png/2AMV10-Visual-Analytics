# Movie Analytics Dashboard

This project is a Dash-based web application for visual analytics of movie data, including genre trends, top-rated movies, and more. It was made in pyton 3.10.11 and not tested on other version so please use this version.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/2AMV10-Visual-Analytics.git
cd 2AMV10-Visual-Analytics
```

### 2. (Optional) Create a Virtual Environment
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3.1 Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```
### 3.2 Make .env and use api key for posters.
Request free api key at https://www.omdbapi.com/apikey.aspx
make a ".env" file in the main directory and put the API key in using "OMDB_API_KEY=.........."
save file

### 4. Run the Application
Start the Dash app:
```bash
python app.py
```

The app will be available at [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

## Project Structure
- `app.py` — Main entry point for the Dash app
- `_2AMV10_app/` — Contains all app modules, views, and callbacks
- `requirements.txt` — Python dependencies
- `assets/` — CSS and static assets
- `data/` — Data files

## Notes
- Make sure you have Python 3.8 or higher installed.
- If you add new dependencies, update `requirements.txt` with `pip freeze > requirements.txt`.


