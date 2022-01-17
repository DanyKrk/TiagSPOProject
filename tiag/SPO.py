import networkx as nx
import matplotlib.pyplot as plt
import copy


# G - graf wejsciowy
# L - lewa strona produkcji
# R - prawa strona produkcji
# links - lista krotek, gdzie (a, b) oznacza, ze wierzcholek a w G odpowiada b w L
# Algorytm usuwa cały podgraf L z G i w jego miejsce wstawia R
def single_pushout(G, L, R, links):
    links_map = dict()
    G1 = copy.deepcopy(G)
    L_edges = L.edges
    R_edges = R.edges
    L_nodes = L.nodes
    R_nodes = R.nodes

    for l in links:
        links_map[l[1]] = l[0]

    print(links_map)
    for e in L_edges:
        G1.remove_edge(links_map[e[0]], links_map[e[1]])

    for n in L_nodes:
        if n not in R_nodes:
            G1.remove_node(links_map[n])

    for n in R_nodes:
        if n not in L_nodes:
            i = 0
            while i in G1.nodes:
                i = i + 1

            G1.add_node(i, label=R.nodes[n]["label"])   # adding new nod with label from R
            links_map[n] = i

    for e in R_edges:
        G1.add_edge(links_map[e[0]], links_map[e[1]])

    return G, G1
# end def
