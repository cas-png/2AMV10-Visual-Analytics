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

    # Create the Folium map
    m = folium.Map(location=[39.5, -165.5], zoom_start=7, tiles='CartoDB positron')

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

    folium.LayerControl().add_to(m)

    # Save the map to the data directory
    map_path = Path(__file__).resolve().parent.parent.parent / "data" / "oceanus_interactive_map.html"
    m.save(map_path)
    return str(map_path)