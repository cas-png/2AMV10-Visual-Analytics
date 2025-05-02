import folium
import json
from pathlib import Path

def generate_map():
    # Dynamically resolve the path to the GeoJSON file
    geojson_path = Path(__file__).resolve().parent.parent.parent / "data" / "Oceanus Geography.geojson"
    if not geojson_path.exists():
        raise FileNotFoundError(f"GeoJSON file not found at {geojson_path}")

    # Load the GeoJSON data
    with open(geojson_path, "r") as f:
        geo_data = json.load(f)

    # Create the base map
    m = folium.Map(location=[39.5, -165.5], zoom_start=7, tiles='CartoDB positron', name="Simple View")

    # Add a terrain view layer with attribution
    folium.TileLayer(
        tiles='https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
        name="Terrain View",
        attr="Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors"
    ).add_to(m)

    # Add a satellite view layer with attribution
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        name="Satellite View",
        attr="Tiles © Esri — Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC"
    ).add_to(m)

    # Add the GeoJSON layer
    def style_function(feature):
        kind = feature['properties'].get('*Kind', 'Unknown')
        colors = {
            'Island': '#a6cee3',
            'Fishing Ground': '#1f78b4',
            'Ecological Preserve': '#33a02c',
            'city': '#fb9a99',
            'buoy': '#ff7f00'
        }
        return {
            'fillColor': colors.get(kind, '#b2df8a'),
            'color': colors.get(kind, '#b2df8a'),
            'weight': 2,
            'fillOpacity': 0.5 if feature['geometry']['type'] == 'Polygon' else 0,
        }

    folium.GeoJson(
        geo_data,
        name='Oceanus Features',
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=['Name', 'Description', '*Kind'], aliases=['Name', 'Description', 'Type'])
    ).add_to(m)

    # Add layer control to switch between views
    folium.LayerControl().add_to(m)

    # Save the map to the data directory
    map_path = Path(__file__).resolve().parent.parent.parent / "data" / "oceanus_interactive_map.html"
    m.save(map_path)
    return str(map_path)