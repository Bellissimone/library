from abc import ABC, abstractmethod
from networkx import MultiDiGraph
import json
from Geojson.GeoJson import GeoJson


class ShortestPathGenerator(ABC):
    """
        Interfaccia che verrà implementata da due classi (PathFromPoint e PathFromPolygon) per la creazione del metodo
        principale che crea uno shortest path tra due punti distinti sulla mappa
    """
    @abstractmethod
    def get_shortest_path(self, g: GeoJson, starter_graph: MultiDiGraph, mode: str, coo1: tuple,
                          coo2: tuple, net_type: str) -> json:
        pass

