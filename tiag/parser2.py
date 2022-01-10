import networkx as nx

#funkcja bierze główny graf, graf lewej strony produkcji i stringa z przyporządkowaniem
#
#funcja zwraca listę y przyporządkowania wierzchołków lub None jeśli przyporządkowanie jest błędne

#done - zmienić input(tak, żeby funkcja przyjmowała dane w formacie np. "(0,3),(1,2),(2,5)" - lewa liczba z głównego grafu, prawa z L)
#done - zmieniam output, żeby pasował do funkcji SPO(funkcja musi zwracać listę krotek, gdzie (a, b) oznacza, ze wierzcholek a w G odpowiada b w L)

#To do
# def parseStringForParser2(assignmentStr):
#     tupleList = assignmentStr.split(",")

def assignmentParser(mainGraph, leftGraph, assignment):
    map1 = map(int, assignment.replace('(', '').replace(')', '').split(','))
    vertList = list(map1)

    y = {}  #przypomniałem sobie że istnieją słowniki
    for i in range(0, len(vertList), 2):
        if vertList[i + 1] in y or vertList[i] in y.values():
            print("Każdy wierzchołek może być przyporządkowany do jednego wierzchołka")
            return None
        y[vertList[i + 1]] = vertList[i]

    if len(y) != leftGraph.number_of_nodes():
        print("Przyporządkowanie niezgodne z liczbą wierzchołków grafu lewej strony produkcji")
        return None

    #usuwam warunek na liczbę wierzchołków w głównym grafie bo nie zawsze działa
    # a i tak jest to sprawdzane przy sprawdzaniu czy krawędź istnieje

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


assignment="(1,0),(3,2),(2,1),(4,3)"
assignmentParser(mainGraph, leftGraph, assignment)
#działa jako tako