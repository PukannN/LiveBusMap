import folium
from shapely import wkt
from shapely.geometry import mapping

class MapService:
    @staticmethod
    #Create a base Folium map centered at the given location.
    def create_base_map(location, zoom=12):

        return folium.Map(location, zoom)
    
    @staticmethod
    def add_geojson(folium_map, geom):
        folium.GeoJson(mapping(geom)).add_to(folium_map)


    @staticmethod
    def save_map(folium_map, filename):
        folium_map.save(filename)
