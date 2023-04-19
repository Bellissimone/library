from abc import ABC, abstractmethod
from networkx import MultiDiGraph
import json
from Geojson.GeoJson import GeoJson


class ShortestPathGenerator(ABC):

    @abstractmethod
    def get_shortest_path(self, g: GeoJson, starter_graph: MultiDiGraph, mode: str, coo1: tuple,
                          coo2: tuple, net_type: str) -> json:
        pass

