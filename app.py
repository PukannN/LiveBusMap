from flask import Flask, render_template
from config import CITY, COUNTRY, MAP_ZOOM
from services.osm_service import OSMService
from services.map_service import MapService
import threading
import time

app = Flask(__name__)
osm_service = OSMService()
map_service = MapService()

def background_updates():
    while True:
        time.sleep(8)
        print("Updating object data")
        bus_stops = osm_service.get_bus_stops(CITY, COUNTRY)
        

@app.route('/')
def show_map():
    try:
        print(f"Fetching coordinates for CITY: {CITY}, COUNTRY: {COUNTRY}")
        center_coord = osm_service.get_coordinates(CITY, COUNTRY)
        wkt_data = osm_service.get_wkt(CITY, COUNTRY)

        #print(f"Coordinates fetched: {center_coord}, WKT data: {wkt_data}")
        
        print("Creating base map...")
        folium_map = map_service.create_base_map(center_coord, MAP_ZOOM)
        print("Base map created.")
        
        print("Adding GeoJSON data to the map...")
        map_service.add_geojson(folium_map, wkt_data)
        
        print("GeoJSON data added.")
        
        map_file = 'templates/map.html'
        print(f"Saving map to {map_file}...")
        #map_service.save_map(folium_map, map_file)
        html_map = folium_map._repr_html_()
        print("Map saved successfully.")

        return render_template('map.html', map=html_map) # Fixed the template path
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while generating the map.", 500

if __name__ == '__main__':
    update_thread = threading.Thread(target=background_updates)
    update_thread.daemon = True
    update_thread.start()
    app.run()