import folium
import requests
import streamlit as st
from streamlit.components.v1 import html
import csv

st.set_page_config(
    page_title="Prevista - London",
    page_icon="https://lirp.cdn-website.com/d8120025/dms3rep/multi/opt/social-image-88w.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Define specific places to highlight (example coordinates)
places = {}
csv_file_path = 'resources/places.csv'
with open(csv_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        place = row['Place']
        latitude = float(row['Latitude'])
        longitude = float(row['Longitude'])
        info = row['Info']
        
        is_complete = all(row[field] for field in ['Place', 'Latitude', 'Longitude', 'Info'])
        
        places[place] = {
            'location': (latitude, longitude),
            'info': info,
            'is_complete': is_complete
        }

# Load the London GeoJSON data
@st.cache_data
def load_London_data():
    url = 'https://raw.githubusercontent.com/radoi90/housequest-data/master/london_boroughs.geojson'
    response = requests.get(url)
    geojson_data = response.json()
    return geojson_data

def create_map(london_geojson, places):
    features = london_geojson['features']
    coords = features[0]['geometry']['coordinates'][0]
    
    # Calculate the center based on coordinates
    map_center = [
        (sum(lat for lon, lat in coords) / len(coords),
         sum(lon for lon, lat in coords) / len(coords))
    ]

    # Create the map
    m = folium.Map(location=map_center[0], zoom_start=10.5)

    # Add London boundary with lighter style
    folium.GeoJson(
        london_geojson,
        style_function=lambda x: {'fillColor': 'lightorange', 'color': 'lightorange', 'weight': 0.5}
    ).add_to(m)

    # Add markers for specific places
    for place, details in places.items():
        pin_color = 'green' if details['is_complete'] else 'gray'
        
        folium.Marker(
            location=details["location"],
            popup=folium.Popup(details["info"], max_width=300),
            tooltip=place,
            icon=folium.Icon(color=pin_color, icon='info-sign')
        ).add_to(m)

    return m


def main():
    st.title('London Map - UK')
    st.write("### Delivery Centres & JCP ")

    # Load the London GeoJSON data
    London_geojson = load_London_data()

    # Create the map with places
    m = create_map(London_geojson, places)

    # Render the map in Streamlit using st.components.html or st_folium (if installed)
    folium_html = m._repr_html_()
    html(folium_html, height=600)

if __name__ == '__main__':
    main()


# pip install folium requests streamlit
# python -m streamlit run app.py
# Dev : https://linkedin.com/in/osamatech786
