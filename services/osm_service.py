from OSMPythonTools.overpass import Overpass
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api
from shapely import wkt
from shapely.geometry import mapping

class OSMService:
    def __init__(self):
        self.nominatim = Nominatim()
        self.overpass = Overpass()
        self.api = Api()

    # Return the coordinates of a city/place from the Nominatim API
    def get_coordinates(self, city, country):
        place = self.nominatim.query(f"{city}, {country}")
        data = place.toJSON()[0]
        map_cords = data["lat"], data["lon"]
        print(f"Coordinates of {city}: {map_cords}")
        return map_cords
    
    # Return the WKT string in geom of a city/place from the Nominatim API
    def get_wkt(self, city, country):
        place = self.nominatim.query(f"{city}, {country}", wkt="True")
        wkt_string = place.wkt()
        geom = wkt.loads(wkt_string)
        return geom