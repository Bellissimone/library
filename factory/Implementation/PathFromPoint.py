import networkx as nx
import osmnx as ox
import json
from factory.ShortestPathGenerator import ShortestPathGenerator
from networkx import MultiDiGraph
import matplotlib.pyplot as plt
from Geojson.GeoJson import GeoJson


class PathFromPoint(ShortestPathGenerator):

    @staticmethod
    def _get_json(g: GeoJson, new_graph: MultiDiGraph, coo1: tuple, coo2: tuple) -> json:
        """
            Metodo che preso il grafo senza vincolo, calcola il percorso migliore che collega il punto di partenza
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

    def get_shortest_path(self, g: GeoJson, starter_graph: MultiDiGraph, mode: str, coo1: tuple, coo2: tuple,
                          net_type: str) -> json:
        """
            Questo metodo viene chiamato solo ed esclusivamente quando il vincolo viene rappresentato da uno
            di questi tre valori:
            Point, LineString o MultiLineString.
            Prende in input il grafo iniziale, il GeoJson contenente il vincolo, il tipo di shortest path da
            trovare, le coordinate di partenza e di arrivo e infine il tipo di grafo da considerare per la creazione del
            vincolo.

            In base al tipo di vincolo contenuto nel GeoJson ci sarà un algoritmo differente:
                - Point: quando il vincolo è rappresentato da un punto, verrà trovato il nodo di riferimento più vicino
                    per poi essere eliminato dal grafo generale sul quale verrà applicato l'algoritmo di dijkstra
                    per trovare il cammino minimo.
                - LineString o MultiLinestring: quando il vincolo è rappresentato da una LineString o da
                    una MultiLineString, i punti della LineString/MultiLineString verranno trattati come se fossero una
                    lista di punti singoli e verranno eliminati uno ad uno dal grafo principale per poi
                    applicare Dijkstra per trovare lo shortest path.

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
