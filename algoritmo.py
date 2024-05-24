import networkx as nx
import matplotlib.pyplot as plt

def visualizarNodos(data, numFigura, posX, posY, node_colors=None):
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

    plt.figure(numFigura)
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(posX, posY, 450, 450)  # Establecemos posició y tamaño de la ventana.

    #dibujamos
    if node_colors:
        nx.draw(F, pos, with_labels=True, arrows=False, node_color=[node_colors.get(node, 'blue') for node in F.nodes()])
    else:
        nx.draw(F, pos, with_labels=True, arrows=False)

    plt.title("Grafos con Conexiones")
    plt.pause(3)  # Pausa de 3 segundos
    plt.show()


def visualizarArbol(G, numFigura, inicial, posX, posY, node_colors=None):
    # Limpiar la figura actual
    plt.clf()
    
    # Obtener las posiciones predefinidas de los nodos
    pos = nx.get_node_attributes(G, 'pos')

    fig = plt.figure(numFigura)

     # Reubicar la ventana
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(posX, posY, 450, 450)  # Cambia las coordenadas y el tamaño según lo necesites

    if node_colors:
        nx.draw(G, pos=pos, with_labels=True, arrows=False,
                node_color=[node_colors.get(node, 'blue') for node in G.nodes()])
    else:
        nx.draw(G, pos=pos, with_labels=True, arrows=False)

    plt.pause(1.5)  # Pausa de 3 segundos


def agregar_datos_al_camino(algoritmo_index, nodo, estadisticas):
    estadisticas[1][algoritmo_index] += nodo + ', '


def buscar_padre(camino, nodo_buscar):   #función que se usa para buscar el padre de un nodo en el diccionario del camino.
    for nodo_padre, atributos in camino.items():
        if nodo_buscar in atributos['conexiones']:
            return nodo_padre
    return None


def ejecutar_algoritmos(data, inicial, final):
    estadisticas = [['No', 'No'],  # Se llegó al nodo final [Sí|No]
                    ['', ''],      # Camino recorrido [string]
                    [0, 0]]        # Cant. saltos [int]

    node_colors = {}
    node_colors[inicial] = 'green'
    node_colors[final] = 'orange'

    nivelArbolSimple = 1
    nivelArbolMaxima = 1

    ubicacionEntreHijosSimple = 0
    ubicacionEntreHijosMaxima = 0

    cantidadHijosSimple = 0
    cantidadHijosMaxima = 0

    ubicacionesXsimple = {}
    ubicacionesXmaxima = {}
    ubicacionesXsimple[inicial]=0
    ubicacionesXsimple[final]=0
    ubicacionesXmaxima[inicial]=0
    ubicacionesXmaxima[final]=0

    condicionSimple = False
    condicionMaxima = False

    visualizarNodos(data, "Grafo", 1, 30, node_colors)   #Graficamos todos los nodos en forma de grafo

    camino_simple = {}
    camino_maxima = {}
    

    G = nx.DiGraph()   #variable que guarda el grafico de escalada simple.
    G.add_node(inicial, pos=(float(0), float(0)))
    H = nx.DiGraph()   #variable que guarda el grafico de máxima pendiente
    H.add_node(inicial, pos=(float(0), float(0)))

    # Ejecutar algoritmos
    escaladaSimple(data, inicial, final, camino_simple, estadisticas, 0)
    estadisticas[2][0] = str(estadisticas[2][0])
    maximaPendiente(data, inicial, final, camino_maxima, estadisticas,1)
    estadisticas[2][1] = str(estadisticas[2][1])

    copia_camino_simple = camino_simple
    copia_camino_maxima = camino_maxima

    # Variable para controlar el bucle
    continue_running = True

    while continue_running:   #bucle que se va a recorrer mientras los diccionarios tengan datos.                       

        if not camino_simple:
            condicionSimple = True
        elif condicionSimple != True:            
            primer_elemento_clave_simple, primer_elemento_valor_simple = next(iter(camino_simple.items()))

            if cantidadHijosSimple == 0:   #condición para evitar que cada vez que se dibuja un hijo se cambie el valor

                if primer_elemento_clave_simple != inicial:
                    nivelArbolSimple = nivelArbolSimple + 1   #el nivel define la posición en el eje y del nodo.

                cantidadHijosSimple = len(camino_simple[primer_elemento_clave_simple]['conexiones'])   #rescatamos la cantidad de hijos que tiene para ubicarlos en el eje x
                
                if cantidadHijosSimple % 2 == 0:
                    ubicacionEntreHijosSimple = (cantidadHijosSimple / 2) / -1
                else:
                    ubicacionEntreHijosSimple = ((cantidadHijosSimple / 2) - 0.5) / -1
            else:
                if cantidadHijosSimple % 2 == 0 and ubicacionEntreHijosSimple + 1 == 0:
                    ubicacionEntreHijosSimple = ubicacionEntreHijosSimple + 2
                else:
                    ubicacionEntreHijosSimple = ubicacionEntreHijosSimple + 1

            if not camino_simple[primer_elemento_clave_simple]["conexiones"]:                
                camino_simple.pop(primer_elemento_clave_simple)
                cantidadHijosSimple = 0

            else:             
                G.add_node(primer_elemento_valor_simple["conexiones"][0], pos=(float(ubicacionesXsimple[buscar_padre(copia_camino_simple, primer_elemento_valor_simple["conexiones"][0])] + ubicacionEntreHijosSimple), float(0 - nivelArbolSimple)), weight=5)
                ubicacionesXsimple[primer_elemento_valor_simple["conexiones"][0]] = ubicacionesXsimple[buscar_padre(copia_camino_simple, primer_elemento_valor_simple["conexiones"][0])] + ubicacionEntreHijosSimple
                G.add_edge(primer_elemento_clave_simple, primer_elemento_valor_simple["conexiones"][0])
                G.add_edge(primer_elemento_valor_simple["conexiones"][0], primer_elemento_clave_simple)
                primer_elemento_valor_simple["conexiones"].pop(0)

        if not camino_maxima:
                condicionMaxima = True
        elif condicionMaxima != True:
                primer_elemento_clave_maxima, primer_elemento_valor_maxima = next(iter(camino_maxima.items()))

                if cantidadHijosMaxima == 0:  # condición para evitar que cada vez que se dibuja un hijo se cambie el valor
                    if primer_elemento_clave_maxima != inicial:
                        nivelArbolMaxima += 1  # el nivel define la posición en el eje y del nodo.

                    cantidadHijosMaxima = len(camino_maxima[primer_elemento_clave_maxima]['conexiones'])  # rescatamos la cantidad de hijos que tiene para ubicarlos en el eje x

                    if cantidadHijosMaxima % 2 == 0:
                        ubicacionEntreHijosMaxima = (cantidadHijosMaxima / 2) / -1
                    else:
                        ubicacionEntreHijosMaxima = ((cantidadHijosMaxima / 2) - 0.5) / -1
                else:
                    if cantidadHijosMaxima % 2 == 0 and ubicacionEntreHijosMaxima + 1 == 0:
                        ubicacionEntreHijosMaxima += 2
                    else:
                        ubicacionEntreHijosMaxima += 1

                if not camino_maxima[primer_elemento_clave_maxima]["conexiones"]:
                    camino_maxima.pop(primer_elemento_clave_maxima)
                    cantidadHijosMaxima = 0
                else:
                    H.add_node(primer_elemento_valor_maxima["conexiones"][0], pos=(float(ubicacionesXmaxima[buscar_padre(copia_camino_maxima, primer_elemento_valor_maxima["conexiones"][0])] + ubicacionEntreHijosMaxima), float(0 - nivelArbolMaxima)))
                    ubicacionesXmaxima[primer_elemento_valor_maxima["conexiones"][0]] = ubicacionesXmaxima[buscar_padre(copia_camino_maxima, primer_elemento_valor_maxima["conexiones"][0])] + ubicacionEntreHijosMaxima
                    H.add_edge(primer_elemento_clave_maxima, primer_elemento_valor_maxima["conexiones"][0])
                    H.add_edge(primer_elemento_valor_maxima["conexiones"][0], primer_elemento_clave_maxima)
                    print("Se añadio conexion al nodo:", primer_elemento_valor_maxima["conexiones"][0])
                    primer_elemento_valor_maxima["conexiones"].pop(0)
                


        if condicionSimple == True and condicionMaxima == True:
                continue_running = False
            
            
        if condicionSimple != True:
            visualizarArbol(G, "Escalada Simple", inicial, 450, 30, node_colors)

        if condicionMaxima != True:
            visualizarArbol(H, "Máxima Pendiente", inicial, 900, 30, node_colors)
        
        print("Final del bucle de grafico")

        
    return estadisticas
    

def escaladaSimple(data, inicial, final, camino, estadisticas, algoritmoSeleccionado):
    finalEstadistica = True   #variable que se usa para ver si se llego al nodo final
    explorados = set()
    act = inicial
    agregar_datos_al_camino(algoritmoSeleccionado, inicial, estadisticas)
    next_node = None
    node_colors = {inicial: 'green', final: 'orange'}
    print("Algoritmo seleccionado: Escalada simple")
    #G = nx.DiGraph()
    while act != final:
        if act == final:
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
                camino[act]["conexiones"].append(connection)
                if connection != final and int(data[connection]['valor_heuristico']) < int(costo_actual):
                    next_node = connection
                    break
                elif connection == final:
                    next_node = connection
                    break
        if next_node is None:
            finalEstadistica = False
            print("Hay un mínimo local en:", act)
            node_colors[act] = 'red'
            break
            # Si encontramos un nodo con un costo menor, avanzamos hacia ese nodo
        else:
            act = next_node
            print("El nuevo nodo actual es", act)

            agregar_datos_al_camino(algoritmoSeleccionado, act, estadisticas) 
            estadisticas[2][algoritmoSeleccionado] = estadisticas[2][algoritmoSeleccionado] + 1  
    print("Fin del bucle")

    if finalEstadistica:
        estadisticas[0][algoritmoSeleccionado] = 'Sí'
    else:
        estadisticas[0][algoritmoSeleccionado] = 'No'

def maximaPendiente(data, inicial, final, camino, estadisticas, algoritmoSeleccionado):
    finalEstadistica = True
    explorados = set()
    act = inicial
    agregar_datos_al_camino(algoritmoSeleccionado, inicial, estadisticas)
    next_node = None
    node_colors = {inicial: 'green', final: 'orange'}
    print("Algoritmo seleccionado: Maxima Pendiente")
    while act != final:
        if act == final:
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
                camino[act]["conexiones"].append(connection)
                if connection != final and int(data[connection]['valor_heuristico']) < int(costo_actual):
                    next_node = connection
                    costo_actual = data[next_node]['valor_heuristico']
                elif connection == final:
                    next_node = connection
                    break
        if next_node is None:
            finalEstadistica = False   #variable para ver si se llego al final
            print("Hay un mínimo local en:", act)
            node_colors[act] = 'red'
            break
        else:
            act = next_node
            print("El nuevo nodo actual es", act)

            agregar_datos_al_camino(algoritmoSeleccionado, act, estadisticas) 
            estadisticas[2][algoritmoSeleccionado] = estadisticas[2][algoritmoSeleccionado] + 1  
    print("Fin del bucle")

    if finalEstadistica:
        estadisticas[0][algoritmoSeleccionado] = 'Sí'
    else:
        estadisticas[0][algoritmoSeleccionado] = 'No'
