import requests
from shapely import geometry


class ApiOrs:

    def __init__(self, host: str = "https://api.openrouteservice.org",
                 key: str = "5b3ce3597851110001cf6248c7ba14a31dbc49eb812e3b04d387f59f"):
        self.__host = host
        self.__key = key

    def __auth(self) -> dict:
        auth = {
            "Authorization": self.__key
        }
        return auth

    def get_key(self) -> str:
        return self.__key

    @staticmethod
    def __get_location(coordinates: tuple, distance: float) -> dict:
        return {
            'locations': [[coordinates[0], coordinates[1]]],
            'range': [distance]
        }

    def get_coordinates_from_address(self, address: str, context: str = "geocode") -> tuple:
        response = requests.get(
            f"https://{self.__host}/{context}/search?api_key={self.__key}&text={address}")
        data = response.json()
        return tuple([data["features"]["geometry"]["coordinates"][0], data["features"]["geometry"]["coordinates"][1]])

    def get_duration_from_points(self, mode: str, coo1: tuple, coo2: tuple) -> float:
        response = requests.get(
            f"https://api.openrouteservice.org/v2/directions/{mode}?api_key={self.__key}&start={coo1[0]},"
            f"{coo1[1]}&end={coo2[0]},{coo2[1]}")
        data = response.json()
        return data['features'][0]['properties']['summary']['duration']

    def get_distance_from_points(self, mode: str, coo1: tuple, coo2: tuple) -> float:
        response = requests.get(
            f"https://api.openrouteservice.org/v2/directions/{mode}?api_key={self.__key}&start={coo1[0]},"
            f"{coo1[1]}&end={coo2[0]},{coo2[1]}")
        data = response.json()
        return data['features'][0]['properties']['summary']['distance']

    def get_isochrone_from_point(self, coordinates: tuple, mode: str, distance: float) -> list:
        location = self.__get_location(coordinates, distance)
        isochrone_point_list = []

        response = requests.post(
            f"https://api.openrouteservice.org/v2/isochrones/{mode}",
            json=location,
            headers=self.__auth()
        )

        isochrone = response.json()

        for p in isochrone['features'][0]['geometry']['coordinates'][0]:
            isochrone_point_list.append(geometry.Point(p))

        return isochrone_point_list
