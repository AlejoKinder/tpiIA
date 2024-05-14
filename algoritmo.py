
#import interfaz   # Posiblemente tengamos que hacer al revés, dijo el que se resbaló y cayó de espalda.
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

def agregarGrafo(G, u, v, w = 1, sent = True):
    G.add_edge(u, v, weight = w)

    #si sentido es falso, quiere decir que queremos que sea unidireccional
    if sent:
        G.add_edge(v, u, weight = w)

def visualizarNodos(data, node_colors=None):
    F = nx.DiGraph()  # Crear un nuevo grafo dirigido

    # Agregar todos los nodos al grafo
    for node, properties in data.items():
        F.add_node(node, pos=(float(properties['coord_x']), float(properties['coord_y'])))

    # Agregar las conexiones al grafo (bidireccionales)
    for node, properties in data.items():
        connections = properties['conexiones']
        for connection in connections:
            # Agregar la conexión en ambas direcciones
            F.add_edge(node, connection)
            F.add_edge(connection, node)

    # Obtener las posiciones de los nodos según las coordenadas
    pos = nx.get_node_attributes(F, 'pos')

    # Dibujar el grafo
    if node_colors:
        nx.draw(F, pos, with_labels=True, arrows=False, node_color=[node_colors.get(node, 'blue') for node in F.nodes()])
    else:
        nx.draw(F, pos, with_labels=True, arrows=False)

    plt.title("Grafos con Conexiones")
    plt.pause(5)  # Pausa de 5 segundos
    plt.show()



def visualizarArbol(G, node_colors=None):
    # Obtener la posición de los nodos para dibujar como un árbol
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

    # Limpiar la figura actual
    plt.clf()

    # Dibujar el grafo como un árbol
    if node_colors:
        nx.draw(G, pos, with_labels=True, arrows=False, node_color=[node_colors.get(node, 'blue') for node in G.nodes()])
    else:
        nx.draw(G, pos, with_labels=True, arrows=False)

    plt.title("Grafo como Árbol")
    plt.pause(3)  # Pausa de 3 segundos


def escaladaSimple(data, inicial, final):
    explorados = set()   # Utilizamos un conjunto para los nodos explorados
    camino = set()
    act = inicial   # Nodo actual
    next_node = None  # Inicializamos next_node con None
    node_colors = {}
    node_colors[inicial] = 'green'
    node_colors[final] = 'orange'

    print("Algoritmo seleccionado: Escalada simple")

    visualizarNodos(data, node_colors)   #Graficamos todos los nodos

    print("Nodo inicial:", inicial)
    print("Nodo final:", final)

    # Creamos la variable que contiene el grafo
    G = nx.DiGraph()

    while act != final:
        print("Estoy en el nodo:", act)   # Depuración

        # Si hemos llegado al nodo final, terminamos el algoritmo
        if act == final:
            print("Nodo final")
            break
        
        # Agregamos el nodo actual a la lista de explorados
        explorados.add(act)
        camino.add(act)

        # Obtenemos el costo del nodo actual
        costo_actual = data[act]['valor_heuristico']

        # Obtenemos las conexiones del nodo actual
        connections_str = data[act]['conexiones']
        
        # Verificar si connections_str es una cadena antes de llamar a split()
        if isinstance(connections_str, str):
            connections = connections_str.split(', ')
        else:
            connections = connections_str

        next_node = None

        # Iteramos sobre las conexiones del nodo actual
        for connection in connections:
            # Verificamos si la conexión ya ha sido explorada
            if connection not in explorados:
                explorados.add(connection)
                # Comparamos el costo de la conexión con el mínimo costo actual
                agregarGrafo(G, act, connection)  # Agregar conexión al grafo
                visualizarArbol(G, node_colors)
                if (connection != final):                 
                    if int(data[connection]['valor_heuristico']) < int(costo_actual):                    
                        act = connection
                        next_node = connection
                        break  # Salimos del bucle cuando se encuentra una conexión con un costo más bajo
                else:
                    act = connection
                    next_node = connection
                    break
                    
                
        if next_node is None:
            print("Hay un mínimo local en:", act)
            node_colors[act] = 'red'
            visualizarArbol(G, node_colors)
            break
        # Si encontramos un nodo con un costo menor, avanzamos hacia ese nodo
        else:
            act = next_node
            print("El nuevo nodo actual es", act)

    print("Fin del bucle")


def maximaPendiente(data, inicial, final):
    explorados = set()   # Utilizamos un conjunto para los nodos explorados
    camino = set()
    act = inicial   # Nodo actual
    ss = inicial   #sucesor para el nodo actual
    next_node = None  # Inicializamos next_node con None
    node_colors = {}
    node_colors[inicial] = 'green'
    node_colors[final] = 'orange'

    print("Algoritmo seleccionado: Maxima Pendiente")

    visualizarNodos(data, node_colors)   #Graficamos todos los nodos

    print("Nodo inicial:", inicial)
    print("Nodo final:", final)

    # Creamos la variable que contiene el grafo
    G = nx.DiGraph()

    while act != final:
        print("Estoy en el nodo:", act)   # Depuración

        # Si hemos llegado al nodo final, terminamos el algoritmo
        if act == final:
            print("Nodo final")
            break
        
        # Agregamos el nodo actual a la lista de explorados
        explorados.add(act)
        camino.add(act)

        # Obtenemos el costo del nodo actual
        costo_actual = data[act]['valor_heuristico']

        # Obtenemos las conexiones del nodo actual
        connections_str = data[act]['conexiones']
        
        # Verificar si connections_str es una cadena antes de llamar a split()
        if isinstance(connections_str, str):
            connections = connections_str.split(', ')
        else:
            connections = connections_str

        next_node = None

        # Iteramos sobre las conexiones del nodo actual
        for connection in connections:
            # Verificamos si la conexión ya ha sido explorada
            if connection not in explorados:
                explorados.add(connection)
                # Comparamos el costo de la conexión con el mínimo costo actual
                agregarGrafo(G, act, connection)  # Agregar conexión al grafo
                visualizarArbol(G, node_colors)
                if (connection != final):                 
                    if int(data[connection]['valor_heuristico']) < int(costo_actual):                    
                        ss = connection
                        costo_actual = data[ss]['valor_heuristico']
                        next_node = connection
                        #break  # Salimos del bucle cuando se encuentra una conexión con un costo más bajo
                else:
                    act = connection
                    next_node = connection
                    break              
                
        if next_node is None:
            print("Hay un mínimo local en:", act)
            node_colors[act] = 'red'
            visualizarArbol(G, node_colors)
            break
        # Si encontramos un nodo con un costo menor, avanzamos hacia ese nodo
        else:
            act = next_node
            print("El nuevo nodo actual es", act)

    print("Fin del bucle")
