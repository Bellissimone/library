import json

"""
    File creato per mappare il GeoJson contenete il vincolo da non considerare per trovare lo shortest path
"""


class Property:
    def __init__(self):
        self.prop = ""


class Geometry:

    def __init__(self, coordinates: any, type: str):
        self.coordinates = coordinates
        self.type = type

    def get_coords(self):
        return self.coordinates

    def get_type(self):
        return self.type

    def set_coords(self, coordinates: list):
        self.coordinates = coordinates

    def set_type(self, type: str):
        self.type = type

    def __repr__(self):
        return f"{self.coordinates} - {self.type}"


class GeoJson:

    def __init__(self, g: json):
        self.type = g['type']
        self.property = Property()
        self.geometry = Geometry(g['geometry']['coordinates'], g['geometry']['type'])

    def get_geometry(self):
        return self.geometry

    def get_property(self):
        return self.property

    def get_type(self):
        return self.type

    def set_type(self, t: str):
        self.type = t

    def set_geometry(self, g: Geometry):
        self.geometry = g

    def set_property(self, p: Property):
        self.property = p

    def create_json(self, net_type: str):
        geo_dict = {
            "type": self.type,
            "properties": {
                "type_net": net_type
            },
            "geometry": {
                "coordinates": self.geometry.coordinates,
                "type": "LineString"
            }
        }
        return json.dumps(geo_dict, indent=4)
