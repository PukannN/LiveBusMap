from OSMPythonTools.overpass import Overpass
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api


from shapely import wkt
from shapely.geometry import mapping

import time
from flask import Flask, render_template, jsonify
from threading import Thread

# Initialize API
api = Api()
# Initialize Overpass
overpass = Overpass()
# Initialize Nominatim
nominatim = Nominatim()

city = "Havirov"
country = "Czech Republic"

place = nominatim.query(f"{city}, {country}", wkt="True")

# Reads map data from the Nominatim API
data = place.toJSON()[0]
map_cords = data["lat"], data["lon"]
print(f"Coordinates of {city}: {map_cords}")

# Reads the WKT string from the Nominatim API
# and converts it to a Shapely geometry object

wkt_string = place.wkt()
geom = wkt.loads(wkt_string)
center = map_cords

# Iserts the geometry into a Folium map
folium_map = folium.Map(location=map_cords, zoom_start=13)
folium.GeoJson(mapping(geom)).add_to(folium_map)

# Saves the map to an HTML file
 
folium_map.save("map.html")

# lat, lon = [nomPlace.lat(), nomPlace.lon()]
# print(lan,lon)



# Query for bus stops in Havířov



# # Query for bus relations (routes) in Havířov with ref=M110
# query = '''
#     area[f"name"={town}}]->.searchArea;
#     relation[route="bus"](area.searchArea);
#     out geom;
# '''
# result = overpass.query(query)
# bus_route = result.elements()[0]
# m = folium.Map()

