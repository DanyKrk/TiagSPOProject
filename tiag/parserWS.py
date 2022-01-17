import networkx as nx
import matplotlib.pyplot as plt


# w pliku wejsciowym dwa kolejne wiersze opisują graf
# pierwszy zawiera etykiety wypisane po kolei odzielone ';'
# drugi zawiera krotki oddzielone ';' , reprezentujące krawędzie

def creating_graph(list_nodes,list_edges):
    labels = list_nodes.split(";")
    labels[-1] = labels[-1][:len(labels[-1])-1]
    G = nx.Graph()
    for i in range(len(labels)):
        G.add_node(i, label=labels[i])

    edges = list_edges.split(";")
    for i in range(len(edges)):
        if 0 <= int(edges[i][1]) < len(G.nodes()) and 0 <= int(edges[i][3]) < len(G.nodes()):
            G.add_edge(int(edges[i][1]), int(edges[i][3]))
        else:
            print("ERROR!!!")
            quit()
    return G

def creating_output_list(filepath):  # głowna funkcja
    file = open(filepath, "r")
    graphs = []
    labels = file.readline()
    edges = file.readline()
    while len(labels) > 0 and len(edges)>0:
        graphs.append(creating_graph(labels,edges))
        labels = file.readline()
        edges = file.readline()
    return graphs

