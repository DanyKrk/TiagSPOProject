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

options = {
    "font_size": 10,
    "verticalalignment": "top"

}

options2 = {
    "font_size": 20,
    "verticalalignment": "top",
    "node_size": 1000,
}


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

        self.buttons = GridLayout()
        self.buttons.cols = 2
        self.buttons.rows = 1

        self.button = Button(text="Cofnij transformację")
        self.button.size_hint = (0.3,0.05)
        self.button.bind(on_press=self.undoTransformation)
        self.buttons.add_widget(self.button)

        self.button = Button(text="Wybór transformacji")
        self.button.size_hint = (0.7,0.05)
        self.button.bind(on_press=self.goToChoice)
        self.buttons.add_widget(self.button)

        self.buttons.size_hint = (0.1, 0.05)
        self.add_widget(self.buttons)

    def goToChoice(self,instance): #aktywowana przez przycisk, zmienia screen na wybor transformacji
        main_app.screen_menager.current = "Choice"
        main_app.screen_menager.transition.direction = "left"

    def undoTransformation(self,instance):
        global mainGraph
        global prevGraph
        mainGraph = prevGraph
        plt.close()
        labelstable = nx.get_node_attributes(mainGraph, 'label')
        pos = nx.spring_layout(mainGraph)
        nx.draw_networkx(mainGraph, pos, **options)
        nx.draw_networkx_labels(mainGraph, pos, labels=labelstable, font_size=10, verticalalignment="bottom")
        plt.savefig("maingraph.png")
        self.updateImage()
        plt.close()


    def updateImage(self): #uaktualnia obraz grafu po zrobieniu transformacji
        self.image.reload()



class Choice(Widget):
    #screen z wybieraniem transformacji, należy kliknąć którąś, mozna zmieniac zdanie, liczy sie kliknieta jako ostatnia;
    #należy wpisać indeksowanie, mozna sobie cofać do screena z obrazkiem grafu
    #zatwierdzić przyciskiem w prawym dolnym rogu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.whichTransformation = 1
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
        global prevGraph
        plt.close()

        if (self.whichTransformation > numOfTransformations):
            links,isOk = [],False
            main_app.error.errorType("Wybrano transformację której nie podano w pliku wejściowym")
        else:
            links,isOk = parser2.assignmentParser(mainGraph, leftGraph(self.whichTransformation), self.assignement,main_app)

        if (isOk):
            prevGraph,mainGraph,new_nodes = SPO.single_pushout(mainGraph, leftGraph(self.whichTransformation), rightGraph(self.whichTransformation), links)

            plt.close()
            labelstable = nx.get_node_attributes(mainGraph, 'label')
            pos = nx.spring_layout(mainGraph)
            color_map = []
            for node in mainGraph.nodes:
                if node in new_nodes:
                    color_map.append('red')
                else:
                    color_map.append("C0")
            nx.draw_networkx(mainGraph, pos, node_color=color_map, **options)
            nx.draw_networkx_labels(mainGraph, pos, labels=labelstable, font_size=10, verticalalignment="bottom")
            plt.savefig("maingraph.png")

            main_app.graph_view.updateImage()

            main_app.screen_menager.current = "Graph View"
            main_app.screen_menager.transition.direction = "left"

        else:
            main_app.screen_menager.current = "Error"
            main_app.screen_menager.transition.direction = "up"

    def errorNoticed(self,errorMessage):
        main_app.screen_menager.current = "Error"
        main_app.error.errorType(errorMessage)

    def setWhichTransformation(self,x):
        self.whichTransformation = x

    def setAssignement(self,x):
        self.assignement = x



class Error(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.99, 0.99)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.label = Label(text="Wystąpił błąd: ")
        self.add_widget(self.label)
        self.button = Button(text="Powrót")
        self.button.bind(on_press=self.goToChoice)
        self.add_widget(self.button)

    def errorType(self,message):
        self.label.text="Wystapił błąd: " + message

    def goToChoice(self, instance):
        main_app.screen_menager.current = "Choice"
        main_app.screen_menager.transition.direction = "down"


class MyApp(App):

    def build(self):

        self.screen_menager = ScreenManager()

        self.graph_view = GraphView()
        screen = Screen(name="Graph View")
        screen.add_widget(self.graph_view)
        self.screen_menager.add_widget(screen)

        self.error = Error()
        screen = Screen(name="Error")
        screen.add_widget(self.error)
        self.screen_menager.add_widget(screen)

        self.choice = Choice()
        screen = Screen(name="Choice")
        screen.add_widget(self.choice)
        self.screen_menager.add_widget(screen)

        return self.screen_menager


if __name__ == '__main__':
    global graphs
    global mainGraph
    global prevGraph
    global numOfTransformations
    filepath = "ex3.txt"

    graphs = parserWS.creating_output_list(filepath)
    mainGraph = graphs[0]
    prevGraph = copy.deepcopy(mainGraph)
    numOfTransformations = (len(graphs) - 1)/2

    labelstable = nx.get_node_attributes(mainGraph,'label')
    pos = nx.spring_layout(mainGraph)
    nx.draw_networkx(mainGraph, pos, **options)
    nx.draw_networkx_labels(mainGraph, pos, labels=labelstable, font_size=10, verticalalignment="bottom")
    # plt.axis("off")
    plt.savefig("maingraph.png")

    for i in range(1, len(graphs)):
        plt.close()

        labelstable = nx.get_node_attributes(graphs[i], 'label')
        pos = nx.spring_layout(graphs[i])
        nx.draw_networkx(graphs[i], pos, **options2)
        nx.draw_networkx_labels(graphs[i], pos, labels=labelstable, font_size=20, verticalalignment="bottom")
        if i % 2 == 0:
            plt.savefig("transformacja" + str(int(i/2)) + ".png")
        else:
            plt.savefig("transformacja" + str(int(i/2 + 1)) + "L.png")

    plt.close()
    for i in range(1,13):
        if i > len(graphs)-1:
            if i % 2 == 0:
                plt.savefig("transformacja" + str(int(i / 2)) + ".png")
            else:
                plt.savefig("transformacja" + str(int(i / 2 + 1)) + "L.png")


    plt.close()
    main_app = MyApp()
    main_app.run()