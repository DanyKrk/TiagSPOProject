import networkx as nx

#funkcja bierze główny graf, graf lewej strony produkcji i stringa z przyporządkowaniem
#string jest w formacie y0;y1;yi;.. gdzie yi to indeks w grafie głównym i-tego wierzchołka grafu lewej strony produkcji
#funcja zwraca listę y przyporządkowania wierzchołków lub None jeśli przyporządkowanie jest błędne
def parser2(mainGraph,leftGraph,assignment):

    str_y=assignment.split(";")
    map_y=map(int,str_y)
    y=list(map_y)

    if len(y)!=leftGraph.number_of_nodes():
        print("Przyporządkowanie niezgodne z liczbą wierzchołków grafu lewej strony produkcji")
        return None

    if max(y)>mainGraph.number_of_nodes()-1: #zakładam że w grafie głównym wierzchołki są numerowane od 0 po kolei
        print("Przyporządkowanie niezgodne z liczbą wierzchołków głównego grafu")
        return None

    if len(y)!=len(set(y)):
        print("Każdy wierzchołek musi być przyporządkowany do jednego wierzchołka")
        return None

    for edge in leftGraph.edges:
        if not mainGraph.has_edge(y[edge[0]],y[edge[1]]):
            print("Błędne przyporządkowanie")
            return None

    print("Jest OK")
    return y


#test
mainGraph = nx.Graph()
mainGraph.add_edge(0,1)
mainGraph.add_edge(1,2)
mainGraph.add_edge(2,3)
mainGraph.add_edge(3,4)
mainGraph.add_edge(2,4)

leftGraph = nx.Graph()
leftGraph.add_edge(0,1)
leftGraph.add_edge(1,2)
leftGraph.add_edge(2,3)


assignment="1;2;3;4"
parser2(mainGraph,leftGraph,assignment)
#działa jako tako