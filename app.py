# filepath: c:\Users\20191994\Desktop\DSAI\Visual Analytics\visual analytics\dashframework-main\app.py
from _2AMV10_app.main import app
from _2AMV10_app.views.menu import make_menu_layout
from _2AMV10_app.views.scatterplot import Scatterplot
from _2AMV10_app.views.map import generate_map  # Import the map generation function

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

if __name__ == '__main__':
    # Generate the Folium map and embed it
    map_path = generate_map()
    folium_map = html.Iframe(
        srcDoc=open(map_path, 'r').read(),
        width='100%',
        height='600px'
    )

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    folium_map  # Add the Folium map here
                ],
            ),
        ],
    )

    app.run_server(debug=True, dev_tools_ui=False)