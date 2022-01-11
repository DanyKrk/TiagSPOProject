import networkx as nx
import matplotlib.pyplot as plt

# filepath = "ex1.txt"  # nazwa ścieżki, trzeba zdecydować jak będzię ona wprowadzana

def creating_graph(edges):  # funkcja tworząca graf, (wiersz pliku tekstowego jako dane wejściowe)
    G = nx.Graph()
    nodes = edges.split(";")    # rozdzielanie kolejnych wierzchołków do listy
    for i in range(len(nodes)):
        G.add_node(i)
        for j in range(1, len(nodes[i]) - 1, 2):
            new_edge = int(nodes[i][j])
            if new_edge < len(nodes) and str(i) in nodes[new_edge]:
                G.add_edge(i, new_edge)
            else:
                print("ERROR!!!")
                quit()
    #nx.draw_networkx(G)
    #plt.show()
    return G

def creating_output_list(filepath):  # głowna funkcja
    file = open(filepath, "r")
    graphs = []
    variable = file.readline()
    while len(variable) > 0:
        graphs.append(creating_graph(variable))
        variable = file.readline()
    
    #for _ in range(0, 13):
        #graphs.append(creating_graph(file.readline()))
        
    return graphs

