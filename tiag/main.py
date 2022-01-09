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
import copy

import parserWS
import parser2
import SPO



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

        def leftGraph(transformationID):
            leftGraphId = 2 * transformationID - 1
            return graphs[leftGraphId]

        def rightGraph(transformationID):
            rightGraphID = 2 * transformationID
            return graphs[rightGraphID]

        global mainGraph
        plt.close()


        links = parser2.assignmentParser(mainGraph, leftGraph(self.whichTransformation), self.assignement)

        SPO.single_pushout(mainGraph, leftGraph(self.whichTransformation), rightGraph(self.whichTransformation), links)

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
    filepath = "ex1.txt"  # nazwa ścieżki, trzeba zdecydować jak będzię ona wprowadzana

    graphs = parserWS.creating_output_list(filepath)
    mainGraph = graphs[0]

    options = {
        'node_size': 100,
    }

    nx.draw(mainGraph, with_labels=True)
    plt.savefig("maingraph.png")

    for i in range(1, len(graphs)):
        plt.close()
        nx.draw(graphs[i])
        if i % 2 == 0:
            plt.savefig("transformacja" + str(i-1) + ".png")
        else:
            plt.savefig("transformacja" + str(i) + "L.png")


    plt.close()
    main_app = MyApp()
    main_app.run()