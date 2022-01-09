import networkx as nx

#funkcja bierze główny graf, graf lewej strony produkcji i stringa z przyporządkowaniem
#string jest w formacie y0;y1;yi;.. gdzie yi to indeks w grafie głównym i-tego wierzchołka grafu lewej strony produkcji
#funcja zwraca listę y przyporządkowania wierzchołków lub None jeśli przyporządkowanie jest błędne

#zmienić input(tak, żeby funkcja przyjmowała dane w formacie np. "(0,3),(1,2),(2,5)" - lewa liczba z głównego grafu, prawa z L)
#done - zmieniam output, żeby pasował do funkcji SPO(funkcja musi zwracać listę krotek, gdzie (a, b) oznacza, ze wierzcholek a w G odpowiada b w L)

#To do
# def parseStringForParser2(assignmentStr):
#     tupleList = assignmentStr.split(",")

def assignmentParser(mainGraph, leftGraph, assignment):

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

    assignment_tuples = []
    for i in range(0, len(y)):
        assignment_tuples.append((y[i], i))

    return assignment_tuples


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
assignmentParser(mainGraph, leftGraph, assignment)
#działa jako tako