import networkx as nx


# funkcja bierze główny graf, graf lewej strony produkcji i stringa z przyporządkowaniem
#
# funcja zwraca listę y przyporządkowania wierzchołków lub None jeśli przyporządkowanie jest błędne

# done - zmienić input(tak, żeby funkcja przyjmowała dane w formacie np. "(0,3),(1,2),(2,5)" - lewa liczba z głównego grafu, prawa z L)
# done - zmieniam output, żeby pasował do funkcji SPO(funkcja musi zwracać listę krotek, gdzie (a, b) oznacza, ze wierzcholek a w G odpowiada b w L)

def assignmentParser(mainGraph, leftGraph, assignment):
    map1 = map(int, assignment.replace('(', '').replace(')', '').split(','))
    vertList = list(map1)

    y = {}
    for i in range(0, len(vertList), 2):
        if vertList[i + 1] in y or vertList[i] in y.values():
            errorHandler("Każdy wierzchołek musi być przyporządkowany do dokładnie jednego wierzchołka")
            return None
        y[vertList[i + 1]] = vertList[i]

    if len(y) != leftGraph.number_of_nodes():
        errorHandler("Przyporządkowanie niezgodne z liczbą wierzchołków grafu lewej strony produkcji")
        return None

    for n in y.keys():
        if not leftGraph.has_node(n):
            errorHandler("Błędne przyporządkowanie (wierzchołek nie istnieje w grafie lewej strony produkcji)")
            return None
        if not mainGraph.has_node(y[n]):
            errorHandler("Błędne przyporządkowanie (wierzchołek nie istnieje w grafie głównym)")
            return None
        if leftGraph.nodes[n]['label'] != mainGraph.nodes[y[n]]['label']:
            errorHandler("Błędne przyporządkowanie (niezgodne etykiety wierzchołków)")
            return None

    for edge in leftGraph.edges:
        if not mainGraph.has_edge(y[edge[0]], y[edge[1]]):
            errorHandler("Błędne przyporządkowanie (krawędź nie istnieje w głównym grafie)")
            return None

    print("Jest OK")

    assignment_tuples = []
    for x, y in y.items():
        assignment_tuples.append((y, x))

    return assignment_tuples


def errorHandler(errorMessage):
    print(errorMessage)

    return


# test
mainGraph = nx.Graph()
mainGraph.add_node(0, label="a")
mainGraph.add_node(1, label="a")
mainGraph.add_node(2, label="b")
mainGraph.add_node(3, label="a")
mainGraph.add_node(4, label="a")
mainGraph.add_edge(0, 1)
mainGraph.add_edge(1, 2)
mainGraph.add_edge(2, 3)
mainGraph.add_edge(3, 4)
mainGraph.add_edge(2, 4)

leftGraph = nx.Graph()
leftGraph.add_node(0, label="a")
leftGraph.add_node(1, label="b")
leftGraph.add_node(2, label="a")
leftGraph.add_node(3, label="a")
leftGraph.add_edge(0, 1)
leftGraph.add_edge(1, 2)
leftGraph.add_edge(2, 3)

assignment = "(1,0),(3,2),(2,1),(4,3)"
assignmentParser(mainGraph, leftGraph, assignment)
# działa jako tako
