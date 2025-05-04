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

@app.route('/')
def show_map():
    try:
        center_coord, wkt_data = osm_service.get_coordinates(CITY, COUNTRY)
        
        folium_map = map_service.create_base_map(center_coord, MAP_ZOOM)
        map_service.add_geojson(folium_map, wkt_data)
        
        map_file = 'templates/map.html'
        map_service.save_map(folium_map, map_file)
        
        return render_template('templates/map.html')
    
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while generating the map.", 500

if __name__ == '__main__':
    update_thread = threading.Thread(target=background_updates)
    update_thread.daemon = True
    update_thread.start()
    app.run()