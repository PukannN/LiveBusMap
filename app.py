from flask import Flask, render_template, redirect, url_for, jsonify
from config import CITY, COUNTRY, MAP_ZOOM
from services.osm_service import OSMService
from services.map_service import MapService
import threading
import time

app = Flask(__name__)
osm_service = OSMService()
map_service = MapService()

#marker_position = [0.0, 0.0]

def background_updates():
    while True:
        time.sleep(1000)
    # global marker_position
    # center_coord = osm_service.get_coordinates(CITY, COUNTRY)
    # cords = list(center_coord)
    # cords[0] = float(cords[0])
    # cords[1] = float(cords[1])
    # marker_position = [cords[0], cords[1]]
    # while True:
    #     time.sleep(1)
    #     marker_position[0] += 0
    #     marker_position[1] += 0

@app.route('/')
def show_map():
    try:
        print(f"Fetching coordinates for CITY: {CITY}, COUNTRY: {COUNTRY}")
        center_coord = osm_service.get_coordinates(CITY, COUNTRY)
        wkt_data = osm_service.get_wkt(CITY, COUNTRY)
        

        print("Creating base map...")
        folium_map = map_service.create_base_map(center_coord, MAP_ZOOM)
        print("Base map created.")
        
        print("Adding GeoJSON data to the map...")
        map_service.add_geojson(folium_map, wkt_data)
        
        print("GeoJSON data added.")
        
        map_file = 'templates/map.html'
        print(f"Saving map to {map_file}...")
        print("Map saved successfully.")

        html_map = folium_map._repr_html_()
        return render_template('map.html', map=html_map)
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while generating the map.", 500

# @app.route('/marker_position')
# def get_marker_position():
#     global marker_position
#     return jsonify({'lat': marker_position[0], 'lng': marker_position[1]})

if __name__ == '__main__':
    update_thread = threading.Thread(target=background_updates)
    update_thread.daemon = True
    update_thread.start()
    app.run()