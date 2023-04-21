import networkx as nx
import osmnx as ox
import json
from factory.ShortestPathGenerator import ShortestPathGenerator
from networkx import MultiDiGraph
from Geojson.GeoJson import GeoJson
from shapely import geometry


class PathFromPolygon(ShortestPathGenerator):

    @staticmethod
    def _get_json(g: GeoJson, starter_graph: MultiDiGraph, coo1: tuple, coo2: tuple) -> json:
        start = ox.distance.nearest_nodes(starter_graph, coo1[0], coo1[1])
        end = ox.distance.nearest_nodes(starter_graph, coo2[0], coo2[1])
        a = nx.shortest_path(starter_graph, start, end, weight='length')
        print(starter_graph[a[1]])
        g.geometry.set_coords(a)
        g.geometry.set_type("LineString")
        return g.create_json()

    @staticmethod
    def _get_constraint_graph(g: GeoJson, net_type: str) -> MultiDiGraph:
        constraint_graph = []
        for p in g.geometry.coordinates[0]:
            constraint_graph.append(geometry.Point(p))
        polygon_constraint = geometry.Polygon([[p.x, p.y] for p in constraint_graph])
        return ox.graph_from_polygon(polygon_constraint, network_type=net_type)

    def get_shortest_path(self, g: GeoJson, starter_graph: MultiDiGraph, mode: str, coo1: tuple, coo2: tuple,
                          net_type: str) -> json:
        constraint_graph = self._get_constraint_graph(g, net_type)
        new_graph = starter_graph.copy()
        new_graph.remove_nodes_from(n for n in constraint_graph if n in starter_graph)
        return self._get_json(g, starter_graph, coo1, coo2)

