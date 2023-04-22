import networkx as nx
import osmnx as ox
import json
from factory.ShortestPathGenerator import ShortestPathGenerator
from networkx import MultiDiGraph
from Geojson.GeoJson import GeoJson


class PathFromPoint(ShortestPathGenerator):

    @staticmethod
    def _get_json(g: GeoJson, starter_graph: MultiDiGraph, coo1: tuple, coo2: tuple) -> json:
        start = ox.distance.nearest_nodes(starter_graph, coo1[0], coo1[1])
        end = ox.distance.nearest_nodes(starter_graph, coo2[0], coo2[1])
        g.geometry.set_coords(nx.shortest_path(starter_graph, start, end, weight='length'))
        g.geometry.set_type("LineString")
        return g.create_json()

    def get_shortest_path(self, g: GeoJson, starter_graph: MultiDiGraph, mode: str, coo1: tuple, coo2: tuple,
                          net_type: str) -> json:
        if g.geometry.type == "Point":
            point = [ox.distance.nearest_nodes(starter_graph, g.geometry.coordinates[0], g.geometry.coordinates[1])]
            starter_graph.remove_nodes_from(point)
            return self._get_json(g, starter_graph, coo1, coo2)
        elif g.geometry.type == "MultiLineString":
            multi_point_list = []
            for i in range(len(g.geometry.coordinates)):
                for j in range(len(g.geometry.coordinates[i])):
                    multi_point_list.append(ox.distance.nearest_nodes(starter_graph, g.geometry.coordinates[i][j][0],
                                                                      g.geometry.coordinates[i][j][1]))
                    starter_graph.remove_nodes_from(multi_point_list)
            return self._get_json(g, starter_graph, coo1, coo2)
        else:
            point_list = []
            for i in range(len(g.geometry.coordinates)):
                point_list.append(ox.distance.nearest_nodes(starter_graph, g.geometry.coordinates[i][0],
                                                            g.geometry.coordinates[i][1]))
                starter_graph.remove_nodes_from(point_list)
            return self._get_json(g, starter_graph, coo1, coo2)
