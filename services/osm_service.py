from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
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
        map_cords = [data["lat"], data["lon"]]
        print(f"Coordinates of {city}: {map_cords}")
        return map_cords
    
    # Return the WKT string in geom of a city/place from the Nominatim API
    def get_wkt(self, city, country):
        place = self.nominatim.query(f"{city}, {country}", wkt="True")
        wkt_string = place.wkt()
        return wkt_string

    def get_bus_stops(self, city, country):
        town_name = f'{city}, {country}'
        town = self.nominatim.query(town_name)
        area_id = town.areaId()

        # Construct the Overpass query to get bus routes and their stops
        query = overpassQueryBuilder(
            area=area_id,
            elementType='relation',
            selector='"route"="bus"',
            includeGeometry=False,
        )

        # Execute the query
        result = self.overpass.query(query)

        # Process the results
        bus_routes = result.elements()

        # Print bus routes and their stops
        for route in bus_routes:
            #print(f"Bus Route: {route.tags().get('ref', 'Unknown')} - {route.tags().get('name', 'Unknown')}")
            for member in route.members():
                if member.type() == 'node' and 'highway' in member.tags() and member.tags()['highway'] == 'bus_stop':
                    return f"  Bus Stop: {member.tags().get('name', 'Unknown')} - Lat: {member.lat()}, Lon: {member.lon()}"
                   