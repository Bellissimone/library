import json
import osmnx as ox
from networkx import MultiDiGraph
from Geojson.GeoJson import GeoJson
from Exceptions import CustomExceptions as ex
from APIORS.ApiOrs import ApiOrs as call
from shapely import geometry
from factory.Implementation.PathFromPoint import PathFromPoint
from factory.Implementation.PathFromPolygon import PathFromPolygon


class BoundPathGenerator:
    """
        Variabili:
            - K: Utilizzata per allargare l'ampiezza del poligono in modo tale da considerare più punti
                per trovare il percorso minimo tra il punto di partenza e il punto di arrivo
            - MODE_*: sono tutti i modi disponibili che possono essere passati al metodo
                per trovare tipo di percorso minimo
        Costanti:
            - POLYGON: rappresenta la lista delle geometrie che vengono formate da un poligono
            - POINT_STRING: rappresenta la lista delle geometrie che vengono formate da punti e stringhe
    """

    __POLYGON = ["Polygon", "MultiPolygon"]
    __POINT_STRING = ["Point", "MultiPoint", "LineString", "MultiLineString"]
    __NET_TYPE = {
        "driving-car": "drive",
        "driving-hgv": "drive",
        "foot-walking": "walk",
        "foot-hiking": "walk",
        "wheelchair": "walk",
        "cycling-road": "bike",
        "cycling-regular": "bike",
        "cycling-mountain": "bike",
        "cycling-electric": "bike",
    }

    K = 1.2

    MODE_DRIVING_CAR = "driving-car"
    MODE_DRIVING_HGV = "driving-hgv"
    MODE_FOOT_WALKING = "foot-walking"
    MODE_FOOT_HIKING = "foot-hiking"
    MODE_WHEELCHAIR = "wheelchair"
    MODE_CYCLING_ROAD = "cycling-road"
    MODE_CYCLING_REGULAR = "cycling-regular"
    MODE_CYCLING_MOUNTAIN = "cycling-mountain"
    MODE_CYCLING_ELECTRIC = "cycling-electric"

    def __init__(self, g: json, mode: str):
        self.__call = call()
        self.__mode = mode
        self.__geojson = GeoJson(g)
        self.__start_point = None
        self.__arrive_point = None
        self.__check_geojson_parameter(self.__geojson)

    def get_constant_for_graph(self) -> float:
        return self.K

    def set_constant_for_graph(self, k: float):
        try:
            if 1 <= k <= 1.5:
                self.K = k
        except ex.ConstantValueError:
            print("valore inserito troppo grande -> valore corretto compreso tra 1.1 e 1.5")
        else:
            print("value accepted")

    def __check_geojson_parameter(self, g: GeoJson):
        """
            Metodo che controlla i valori all'interno del geojson.

            Se non sarà un geojson di tipo feature restituirà errore.

            Se il tipo della geometria descritta dal geojson non sarà tra quelle previste
            da geojson.org il metodo restituirà erroe

            Parameters
            ----------
            g : geojson che descrive la geometria contenete il vincolo da  non considerare
                per trovare il cammino minimo tra 2 punti
        """
        if g.type != "Feature":
            raise ValueError("controlla il (key)type->value del GeoJson: FeatureCollection non valido.")

        try:
            if g.geometry.type in self.__POLYGON or g.geometry.type in self.__POINT_STRING:
                pass
        except ex.GeoJsonGeometryTypeError:
            print(f"{g.geometry.type} is not a geometry type. check the geojson format")

    # set methods for points values
    def __set_start_point(self, coordinate: tuple):
        self.__start_point = coordinate

    def __set_start_point_from_address(self, address: str):
        self.__start_point = self.__call.get_coordinates_from_address(address)

    def __set_arrive_point(self, coordinate: tuple):
        self.__arrive_point = coordinate

    def __set_arrive_point_from_address(self, address: str):
        self.__arrive_point = self.__call.get_coordinates_from_address(address)

    def __set_points(self, coo1: any, coo2: any):
        """
            Metodo che controlla il tipo dei due punti passati alla funzione di creazione del cammino minimo:

            Verranno accettati solo stringhe o tuple altrimenti la funzione restituirà un errore.

            Se la coordinata iniziale/finale sarà una stringa ad esempio "via roma 13, pescara" questa verrà trasformata
            in una tupla  contenente (longitudine, latitudine) del punto sulla mappa e salvata nella variabile di classe
            start_point / arrive_point.

            Se la coordinata iniziale/finale sarà una tupla contenente (longitudine, latitudine) questa verrà salvata nella
            variabile di classe start_point/arrive_point


            Parameters
            ----------
            coo1 : prima coordinata
            coo2 : seconda coordinata
        """
        if type(coo1) is str:
            self.__set_start_point_from_address(coo1)
        if type(coo1) is tuple:
            self.__set_start_point(coo1)
        if type(coo2) is str:
            self.__set_arrive_point_from_address(coo2)
        if type(coo2) is tuple:
            self.__set_arrive_point(coo2)

    def __get_graph_from_point(self, coo1: tuple, coo2: tuple, mode) -> MultiDiGraph:
        """
            Metodo che costruisce il grafo iniziale tra 2 punti passati come parametri,
             utilizzando il punto di partenza (coo1) come punto di partenza di costruzione del grafo.
            Metodo privato che viene richiamato dal metodo pubblico get_bound_path:
                1. calcola la distanza tra i due punti utilizzando una chiamata al server Open Route Service
                2. amplifica la distanza tra i due punti di K (costante) per avere un grafo maggiore
                 su cui calcolare il cammino minimo tra  i due punti
                3. calcolo l'isochrone dal primo punto con distanza * K in modo tale
                 da avere i punti estremi del poligono totale
                4. creo il grafo finale attraverso la libreria osmnx che, passati dei punti estremi di un poligono,
                 crea un grafo contenente tutti i nodi e gli archi che si trovano all'interno di esso.
                5. il grafo iniziale creato ha a disposizione tutti i nodi che distano dal nodo iniziale <= distanza * K


            Parameters
            ----------
            coo1 : prima coordinata
            coo2 : seconda coordinata
            mode : parametro che indica il tipo percorso da trovare, ad esempio un percorso a piedi, in bici ecc..

            Returns
            -------
            MultiDiGraph : è un grafo contenente nodi e archi dell'area geografica di riferimento dati i 2 punti.
                            nodi: incroci o cambi di direzione nelle strade
                            archi: strade che collegano i nodi
        """
        distance = self.__call.get_distance_from_points(mode, coo1, coo2) * self.K
        isochrone_points = self.__call.get_isochrone_from_point(coo1, mode, distance)
        polygon_area = geometry.Polygon([[p.x, p.y] for p in isochrone_points])
        starter_graph = ox.graph_from_polygon(polygon_area, network_type=self.__NET_TYPE[mode])
        return starter_graph

    def get_bound_path(self, coo1: any, coo2: any) -> json:
        """
            Metodo che costruisce il cammino minimo tra 2 punti passati come parametro.
                1. vengono settate le coordinate dei punti dal metodo privato set_points.
                2. viene creato il grafo iniziale all'interno del quale verrà cercato il cammino minimo
                 tra il punto di partenza e il punto di arrivo passati come parametri alla funzione.
                3. viene controllato il tipo di vincolo da non considerare per cercare il cammino minimo.
                    3.1 POLYGON / MUTIPOLYGON => verrà chiamato il metodo per gestire un vincolo di tipo poligono.
                    3.2 POINT / MULTIPOINT / LINESTRING / MULTILINESTRING => verrà chiamato il metodo che gestisce
                        i vincoli contenenti punti e stringhe.



            These points can be:
                - An address like "Via Roma, 14 Pescara"
                - a Tuple that contain coordinates like coo1 = (14.214380353256928, 42.466981383166086)

            Parameters
            ----------
            coo1 : prima coordinata => str ("via Roma 14, pescara") / tuple (14.214380353256928, 42.466981383166086)
            coo2 : seconda coordinata => str ("via Roma 14, pescara") / tuple (14.214380353256928, 42.466981383166086)

            Returns
            -------
            json(geojson) : è un geojson (www.geojson.org) all'interno del quale nella sezione geometry troviamo
                            le coordinate che formeranno il cammino minimo tra i 2 punti senza passare per
                            il vincolo iniziale (polygon, string, point ecc..).
        """
        self.__set_points(coo1, coo2)
        starter_graph = self.__get_graph_from_point(self.__start_point, self.__arrive_point, self.__mode)
        if self.__geojson.geometry.type in self.__POLYGON:
            return PathFromPolygon().get_shortest_path(self.__geojson, starter_graph, self.__mode, coo1, coo2,
                                                       self.__NET_TYPE[self.__mode])
        else:
            return PathFromPoint().get_shortest_path(self.__geojson, starter_graph, self.__mode, coo1, coo2,
                                                     self.__NET_TYPE[self.__mode])
