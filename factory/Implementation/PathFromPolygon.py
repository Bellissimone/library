import networkx as nx
import osmnx as ox
import json
from factory.ShortestPathGenerator import ShortestPathGenerator
from networkx import MultiDiGraph, Graph
from Geojson.GeoJson import GeoJson
from shapely import geometry
import matplotlib.pyplot as plt


class PathFromPolygon(ShortestPathGenerator):

    @staticmethod
    def _get_json_shortest_path(g: GeoJson, new_graph: MultiDiGraph, coo1: tuple, coo2: tuple) -> json:
        """
            Metodo statico chiamato dal metodo principale get_shortest_path.
            Preso il grafo senza vincolo, calcola il percorso migliore che collega il punto di partenza
            con il punto di arrivo e restituisce tutti i nodi del percorso sulla mappa sotto forma di json

            Parameters
            ----------
            g: GeoJson da restituire all'interno del quale troveremo lo shortest path
            new_graph: un grafo di tipo Graph senza il vincolo contenuto nel geojson
            coo1: punto di partenza
            coo2: punto di arrivo

            Returns
            -------
            Json: GeoJson all'interno del quale troviamo il percorso ottimo tra i due punti sulla mappa
        """
        start = ox.distance.nearest_nodes(new_graph, coo1[0], coo1[1])
        end = ox.distance.nearest_nodes(new_graph, coo2[0], coo2[1])
        shortest_path = nx.shortest_path(new_graph, start, end, weight='length')
        # stampa del grafo con il cammino minimo di riferimento --------------------------------------------------
        color_list_constraint_graph = ["r" if node == start or node == end else "g" for node in new_graph.nodes()]
        color_list_shortest_path = ["b" if node in shortest_path else "g" for node in new_graph.nodes()]
        new_g = ox.plot_graph(new_graph, node_color=color_list_constraint_graph)
        shortest_p = ox.plot_graph(new_graph, node_color=color_list_shortest_path)
        new_g = plt.subplots()
        shortest_p = plt.subplots()
        plt.show()
        # --------------------------------------------------------------------------------------------------------
        g.geometry.set_coords(shortest_path)
        g.geometry.set_type("LineString")
        return g.create_json()

    @staticmethod
    def _get_polygons_constraint(g: GeoJson, net_type: str) -> list:
        """
            Metodo che preso il vincolo all'interno del GeoJson lo trasforma in un grafo.
            Questo metodo viene chiamato dal metodo get_shortest_path:
                il grafo creato da questo metodo verrà utilizzato percercare il cammino minimo dal metodo
                 get_json_shortest_path

            Parameters
            ----------
            g: GeoJson che contiene il tipo di vincolo da trasformare in grafo.
            net_type: indica il tipo di grafo da considerare durante la creazione(walk, drive, bike)

            Returns
            -------
            MultiDiGraph: Vincolo sotto forma di grafo
        """
        polygons = []
        for i in range(len(g.geometry.coordinates)):
            polygon_constraint = []
            constraint_points = []
            for p in g.geometry.coordinates[i]:
                constraint_points.append(geometry.Point(p))
            polygon_constraint = geometry.Polygon([[p.x, p.y] for p in constraint_points])
            polygons.append(ox.graph_from_polygon(polygon_constraint, network_type=net_type))

        return polygons

    def get_shortest_path(self, g: GeoJson, starter_graph: MultiDiGraph, mode: str, coo1: tuple, coo2: tuple,
                          net_type: str) -> json:
        """
            Questo metodo viene chiamato solo ed esclusivamente quando il vincolo viene rappresentato da uno
             di questi due valori:
            Polygon, MultiPolygon.
            Metodo che prende in input il grafo iniziale, il GeoJson contenente il vincolo, il tipo di shortest path da
            trovare, le coordinate di partenza e di arrivo e infine il tipo di grafo da considerare per la creazione del
            vincolo

            In base al tipo di vincolo contenuto nel GeoJson ci sarà un algoritmo differente:
            - Polygon: Il vincolo espresso dal poligono verrà trasformato in un grafo e successivamente verrà sottratto
                dal grafo principale per poi applicare Dijkstra e trovare il cammino minimo.
            - MultiPolygon: ci saranno più poligoni come vincoli che,uno ad uno, verrano trasformati in un grafo per poi
                essere sottratti al grafo principale. Infine verrà applicato Dijkstra per trovare lo shortest path.

            Parameters
            ----------
            g: GeoJson contenente il vincolo da togliere sulla mappa per cercare lo shortest path tra il punto di arrivo
                e il punto di partenza
            starter_graph: Grafo iniziale
            mode: il tipo di shortest path da trovare (bici, macchina ecc..)
            coo1: punto di partenza
            coo2: punto di arrivo
            net_type: indica il tipo di grafo da considerare durante la creazione(walk, drive, bike)

            Returns
            -------
            Json: GeoJson all'interno del quale troviamo il percorso ottimo tra i due punti sulla mappa
        """
        polygons_constraint = self._get_polygons_constraint(g, net_type)
        for polygon in polygons_constraint:
            starter_graph.remove_nodes_from(n for n in polygon if n in starter_graph)
        return self._get_json_shortest_path(g, starter_graph, coo1, coo2)
