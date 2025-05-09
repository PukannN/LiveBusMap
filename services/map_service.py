import folium
import folium.map
from shapely import wkt
from shapely.geometry import mapping

class MapService:
    @staticmethod
    #Create a base Folium map centered at the given location.
    def create_base_map(location, zoom=12,):
        return folium.Map(
            location=location,
            zoom_start=zoom, 
            width=1000, 
            height=800,
            min_zoom=12,
            )
    
    @staticmethod
    def add_geojson(folium_map, wkt_string):
        geom = wkt.loads(wkt_string)
        return folium.GeoJson(mapping(geom)).add_to(folium_map)

    @staticmethod
    def save_map(folium_map, filename):
        return folium_map.save(filename)

    @staticmethod
    def add_marker(folium_map, location, popup_text,):
        folium.map.Marker(
            location=location,
            popup=popup_text,
        ).add_to(folium_map)
        return folium_map
