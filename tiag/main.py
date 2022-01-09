import kivy
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager,Screen

from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


Builder.load_file('my.kv')


import networkx as nx
import matplotlib.pyplot as plt



class GraphView(GridLayout): #screen przedstawiający duży obrazek grafu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.99, 0.99)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.image = Image(source="maingraph.png")
        self.image.keep_ratio = True
        self.image.allow_stretch = True
        self.add_widget(self.image)

        self.button = Button(text="Wybór transformacji")
        self.button.size_hint = (0.1,0.05)
        self.button.bind(on_press=self.goToChoice)
        self.add_widget(self.button)


    def goToChoice(self,instance): #aktywowana przez przycisk, zmienia screen na wybor transformacji
        main_app.screen_menager.current = "Choice"
        main_app.screen_menager.transition.direction = "left"

    def updateImage(self): #uaktualnia obraz grafu po zrobieniu transformacji
        self.image.reload()


class Choice(Widget):
    #screen z wybieraniem transformacji, należy kliknąć którąś, mozna zmieniac zdanie, liczy sie kliknieta jako ostatnia;
    #należy wpisać indeksowanie, mozna sobie cofać do screena z obrazkiem grafu
    #zatwierdzić przyciskiem w prawym dolnym rogu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.whichTransformation = 0
        self.assignement = ""

    def goToGraphView(self): #umożliwia podglad grafu podczas wpisywania indeksowania
        main_app.screen_menager.current = "Graph View"
        main_app.screen_menager.transition.direction = "right"

    def transform(self): #wykonuje transformację i przełącza na screen z przetransformowanym grafem
        global mainGraph
        plt.close()

        print(self.whichTransformation)  #te dwa printy wywalić
        print(self.assignement)
        """
        Algorytm zmieniający mainGraph wedle przyjętej transformacji
        
        self.self.whichTransformation to int wskazujący wybraną przez użytkownika transformacje
        ustala sie po zatwierdzeniu przyciskiem
        nalezy wybrac transformacje z odpowiedniej pozycji w liscie transformacji
        
        self.assignement to string wpisanego przez użytkownica indeksowania, sktory powinien byc parsowany parserem2
        
        Przykładowo zrobiłem dodanie jednej krawdzei ale wiadomo, tu ma być allgorytm:
        """
        mainGraph.add_edge(1, 6) #wywalić
        """"""


        nx.draw(mainGraph, with_labels=True)
        plt.savefig("maingraph.png")

        main_app.graph_view.updateImage()

        main_app.screen_menager.current = "Graph View"
        main_app.screen_menager.transition.direction = "left"

    def setWhichTransformation(self,x):
        self.whichTransformation = x

    def setAssignement(self,x):
        self.assignement = x


class MyApp(App):

    def build(self):

        self.screen_menager = ScreenManager()

        self.graph_view = GraphView()
        screen = Screen(name="Graph View")
        screen.add_widget(self.graph_view)
        self.screen_menager.add_widget(screen)

        self.choice = Choice()
        screen = Screen(name="Choice")
        screen.add_widget(self.choice)
        self.screen_menager.add_widget(screen)

        return self.screen_menager





if __name__ == '__main__':
    global graphs
    global mainGraph
    """
    Parser pliku tekstowego:
        zapisać grafy z pliku jako lista graphs
        zapisać graf główny jako mainGraph - jak niżej
        
    """

    graphs = [nx.Graph()]
    mainGraph = graphs[0]



    # przykładowy graf - usunąć gdy będzie działał input
    mainGraph.add_edge(1, 2)
    mainGraph.add_edge(2, 3)
    mainGraph.add_edge(3, 4)
    mainGraph.add_edge(1, 4)
    mainGraph.add_edge(1, 5)
    #


    options = {
        'node_size': 100,
    }

    nx.draw(mainGraph, with_labels=True)
    plt.savefig("maingraph.png")

    """
    tutaj sugeruje jakiegos fora który "i" od 0 do długość tablicy graphs a w środku robi brrr:
        plt.close() - czyści matplotliba na ktorym sie robi graf
        nx.draw(graphs[i]) - robi takie brr brr żeby sie dało graf wyeksportować do obrazka
        plt.savefig("transformacja" + str(i) + ".png") - musimy zaktualizować obrazki przedstawiające kolejne transformacje, wg takiego schematu, bo pozniej uzywam ich nazw zeby je wyswitelic w choice
                lub
        plt.savefig("transformacja" + str(i) + "L.png") - gdy jest to lewa strona transformacji
        
    generalnie obrazki z lewa strona maja nazwy transformacja1L.png, a z prawa po prostu transformacja1.png
    nie zaimplementowałem tej petli bo nie wiem jaka jest konwencja z lista grafów
        
    """


    plt.close()
    main_app = MyApp()
    main_app.run()