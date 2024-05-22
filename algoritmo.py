import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import pprint
import time

def agregarGrafo(G, u, v, w = 1, sent = True):
    G.add_edge(u, v, weight = w)

    #si sentido es falso, quiere decir que queremos que sea unidireccional
    if sent:
        G.add_edge(v, u, weight = w)

def visualizarNodos(data, numFigura, node_colors=None):
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
    plt.figure(numFigura)
    if node_colors:
        nx.draw(F, pos, with_labels=True, arrows=False, node_color=[node_colors.get(node, 'blue') for node in F.nodes()])
    else:
        nx.draw(F, pos, with_labels=True, arrows=False)

    plt.title("Grafos con Conexiones")
    plt.pause(3)  # Pausa de 5 segundos
    plt.show()



def visualizarArbol(G, numFigura, pausa, node_colors=None):
    # Obtener la posición de los nodos para dibujar como un árbol
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

    # Limpiar la figura actual
    plt.clf()

    # Dibujar el grafo como un árbol
    plt.figure(numFigura)
    if node_colors:
        nx.draw(G, pos, with_labels=True, arrows=False, node_color=[node_colors.get(node, 'blue') for node in G.nodes()])
    else:
        nx.draw(G, pos, with_labels=True, arrows=False)

    plt.title("Grafo como Árbol")
    plt.pause(3)  # Pausa de 3 segundos 



def ejecutar_algoritmos(data, inicial, final):
    node_colors = {}
    node_colors[inicial] = 'green'
    node_colors[final] = 'orange'

    visualizarNodos(data, 1, node_colors)   #Graficamos todos los nodos

    camino_simple = {}
    camino_maxima = {}

    G = nx.DiGraph()
    H = nx.DiGraph()

    print("nodo inicial y final: ", inicial, final)

    # Ejecutar algoritmos
    escaladaSimple(data, inicial, final, camino_simple)
    maximaPendiente(data, inicial, final, camino_maxima)

    # Variable para controlar el bucle
    continue_running = True

    while continue_running:
        condicionSimple = False
        condicionMaxima = False


        pprint.pprint(camino_simple)   #depuracion

        if not camino_simple:
            print("no entre a la primera condición")
            condicionSimple = True
        elif condicionSimple != True:
            primer_elemento_clave_simple, primer_elemento_valor_simple = next(iter(camino_simple.items()))
            print(f"Primera clave: {primer_elemento_clave_simple}, Primer valor: {primer_elemento_valor_simple}")

            if not camino_simple[primer_elemento_clave_simple]["conexiones"]:                
                camino_simple.pop(primer_elemento_clave_simple)
            else:
                agregarGrafo(G, primer_elemento_clave_simple, primer_elemento_valor_simple["conexiones"][0])
                print("Se añadio conexion al nodo:", primer_elemento_valor_simple["conexiones"][0])
                primer_elemento_valor_simple["conexiones"].pop(0)

        pprint.pprint(camino_maxima)   #depuracion

        if not camino_maxima:
            print("no entre a la primera condición")
            condicionMaxima = True
        elif condicionMaxima != True:
            primer_elemento_clave_maxima, primer_elemento_valor_maxima = next(iter(camino_maxima.items()))
            print(f"Primera clave: {primer_elemento_clave_maxima}, Primer valor: {primer_elemento_valor_maxima}")

            if not camino_maxima[primer_elemento_clave_maxima]["conexiones"]:                
                camino_maxima.pop(primer_elemento_clave_maxima)
            else:
                agregarGrafo(H, primer_elemento_clave_maxima, primer_elemento_valor_maxima["conexiones"][0])
                print("Se añadio conexion al nodo:", primer_elemento_valor_maxima["conexiones"][0])
                primer_elemento_valor_maxima["conexiones"].pop(0)
            


        if condicionSimple == True and condicionMaxima == True:
            continue_running = False
        
        
        visualizarArbol(G, 2, False, node_colors)
        visualizarArbol(H, 3, True, node_colors)
        #time.sleep(3)
        #plt.pause(3)  # Pausa de 3 segundos

    
    print("Final del bucle de grafico")
    

def escaladaSimple(data, inicial, final, camino):
    explorados = set()
    act = inicial
    next_node = None
    node_colors = {inicial: 'green', final: 'orange'}
    print("Algoritmo seleccionado: Escalada simple")
    #G = nx.DiGraph()
    while act != final:
        print("Estoy en el nodo:", act)
        if act == final:
            print("Nodo final")
            break
        explorados.add(act)
        camino[act] = {"conexiones": []}
        costo_actual = data[act]['valor_heuristico']
        connections = data[act]['conexiones']
        if isinstance(connections, str):
            connections = connections.split(', ')
        next_node = None
        for connection in connections:
            if connection not in explorados:
                explorados.add(connection)
                #agregarGrafo(G, act, connection)
                camino[act]["conexiones"].append(connection)
                #visualizarArbol(G, 2, node_colors)
                if connection != final and int(data[connection]['valor_heuristico']) < int(costo_actual):
                    next_node = connection
                    break
                elif connection == final:
                    next_node = connection
                    break
        if next_node is None:
            print("Hay un mínimo local en:", act)
            node_colors[act] = 'red'
            #visualizarArbol(G, node_colors)
            break
        # Si encontramos un nodo con un costo menor, avanzamos hacia ese nodo
        else:
            act = next_node
            print("El nuevo nodo actual es", act)
    print("Fin del bucle")

def maximaPendiente(data, inicial, final, camino):
    explorados = set()
    act = inicial
    next_node = None
    node_colors = {inicial: 'green', final: 'orange'}
    print("Algoritmo seleccionado: Maxima Pendiente")
    #H = nx.DiGraph()
    while act != final:
        print("Estoy en el nodo:", act)
        if act == final:
            print("Nodo final")
            break
        explorados.add(act)
        camino[act] = {"conexiones": []}
        costo_actual = data[act]['valor_heuristico']
        connections = data[act]['conexiones']
        if isinstance(connections, str):
            connections = connections.split(', ')
        next_node = None
        for connection in connections:
            if connection not in explorados:
                explorados.add(connection)
                #agregarGrafo(H, act, connection)
                camino[act]["conexiones"].append(connection)
                #visualizarArbol(H, 3, node_colors)
                if connection != final and int(data[connection]['valor_heuristico']) < int(costo_actual):
                    next_node = connection
                    costo_actual = data[next_node]['valor_heuristico']
                elif connection == final:
                    next_node = connection
                    break
        if next_node is None:
            print("Hay un mínimo local en:", act)
            node_colors[act] = 'red'
            #visualizarArbol(G, node_colors)
            break
        # Si encontramos un nodo con un costo menor, avanzamos hacia ese nodo
        else:
            act = next_node
            print("El nuevo nodo actual es", act)
    print("Fin del bucle")
