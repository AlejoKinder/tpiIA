import networkx as nx
import matplotlib.pyplot as plt

def visualizarNodos(datos, numFigura, posX, posY, colores_nodo=None):
    F = nx.DiGraph()  # Crear un nuevo grafo dirigido

    # Agregar todos los nodos al grafo
    for nodo, propiedades in datos.items():
        F.add_node(nodo, pos=(float(propiedades['coord_x']), float(propiedades['coord_y'])))

    # Agregar las conexiones al grafo (bidireccionales)
    for nodo, propiedades in datos.items():
        conexiones = propiedades['conexiones']
        for conexion in conexiones:
            # Agregar la conexión en ambas direcciones
            F.add_edge(nodo, conexion)
            F.add_edge(conexion, nodo)

    # Obtener las posiciones de los nodos según las coordenadas
    pos = nx.get_node_attributes(F, 'pos')

    plt.figure(numFigura)
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(posX, posY, 450, 450)  # Establecemos posició y tamaño de la ventana.

    #dibujamos
    if colores_nodo:
        nx.draw(F, pos, with_labels=True, arrows=False, node_color=[colores_nodo.get(node, 'blue') for node in F.nodes()])
    else:
        nx.draw(F, pos, with_labels=True, arrows=False)

    plt.title("Grafos con Conexiones")
    plt.pause(3)  # Pausa de 3 segundos
    plt.show()


def visualizarArbol(G, numFigura, inicial, posX, posY, colores_nodo=None):
    # Limpiar la figura actual
    plt.clf()
    
    # Obtener las posiciones predefinidas de los nodos
    pos = nx.get_node_attributes(G, 'pos')

    fig = plt.figure(numFigura)

     # Reubicar la ventana
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(posX, posY, 450, 450)  # Cambia las coordenadas y el tamaño según lo necesites

    if colores_nodo:
        nx.draw(G, pos=pos, with_labels=True, arrows=False,
                node_color=[colores_nodo.get(node, 'blue') for node in G.nodes()])
    else:
        nx.draw(G, pos=pos, with_labels=True, arrows=False)

    plt.pause(1.5)  # Pausa de 1.5 segundos

def cerrarFiguras(numFigura):
    plt.figure(numFigura)
    plt.close()


def agregar_datos_al_camino(algoritmo_index, nodo, estadisticas):
    estadisticas[1][algoritmo_index] += nodo + ', '


def buscar_padre(camino, nodo_buscar):   #función que se usa para buscar el padre de un nodo en el diccionario del camino.
    for nodo_padre, atributos in camino.items():
        if nodo_buscar in atributos['conexiones']:
            return nodo_padre
    return None


def ejecutar_algoritmos(datos, inicial, final):
    
    #cerramos todas las figuras.
    cerrarFiguras("Grafo")
    cerrarFiguras("Escalada Simple")
    cerrarFiguras("Máxima Pendiente")


    estadisticas = [['No', 'No'],  # Se llegó al nodo final [Sí|No]
                    ['', ''],      # Camino recorrido [string]
                    [0, 0],         # Cant. saltos [int]
                    [1, 1]]        # Cant. pasos [int]

    colores_nodo = {}
    colores_nodo[inicial] = 'green'
    colores_nodo[final] = 'orange'

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

    visualizarNodos(datos, "Grafo", 1, 30, colores_nodo)   #Graficamos todos los nodos en forma de grafo

    camino_simple = {}
    camino_maxima = {}
    

    G = nx.DiGraph()   #variable que guarda el grafico de escalada simple.
    G.add_node(inicial, pos=(float(0), float(0)))
    H = nx.DiGraph()   #variable que guarda el grafico de máxima pendiente
    H.add_node(inicial, pos=(float(0), float(0)))

    if(inicial == final):   #si el  nodo inicial es el final, grafica directamente.
        visualizarArbol(G, "Escalada Simple", inicial, 450, 30, colores_nodo)
        visualizarArbol(H, "Máxima Pendiente", inicial, 900, 30, colores_nodo)


    # Ejecutar algoritmos
    escaladaSimple(datos, inicial, final, camino_simple, estadisticas, 0)
    estadisticas[2][0] = str(estadisticas[2][0])
    maximaPendiente(datos, inicial, final, camino_maxima, estadisticas,1)
    estadisticas[2][1] = str(estadisticas[2][1])

    copia_camino_simple = camino_simple
    copia_camino_maxima = camino_maxima
    # Variable para controlar el bucle
    seguir_ejecutando = True

    while seguir_ejecutando:   #bucle que se va a recorrer mientras los diccionarios tengan datos.                       

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
                estadisticas[3][0] += 1

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
                    estadisticas[3][1] += 1
                


        if condicionSimple == True and condicionMaxima == True:
                seguir_ejecutando = False
            
            
        if condicionSimple != True:
            visualizarArbol(G, "Escalada Simple", inicial, 450, 30, colores_nodo)

        if condicionMaxima != True:
            visualizarArbol(H, "Máxima Pendiente", inicial, 900, 30, colores_nodo)
        
        print("Final del bucle de grafico")

    estadisticas[3][0] = str(estadisticas[3][0])
    estadisticas[3][1] = str(estadisticas[3][1])
    return estadisticas
    

def escaladaSimple(datos, inicial, final, camino, estadisticas, algoritmoSeleccionado):
    finalEstadistica = True   #variable que se usa para ver si se llego al nodo final
    explorados = set()
    act = inicial
    agregar_datos_al_camino(algoritmoSeleccionado, inicial, estadisticas)
    siguiente_nodo = None
    colores_nodo = {inicial: 'green', final: 'orange'}
    print("Algoritmo seleccionado: Escalada simple")

    while act != final:
        if act == final:
            break
        explorados.add(act)     
        camino[act] = {"conexiones": []}
        costo_actual = datos[act]['valor_heuristico']
        conexiones = datos[act]['conexiones']
        if isinstance(conexiones, str):
            conexiones = conexiones.split(', ')
        siguiente_nodo = None
        for conexiones in conexiones:
            if conexiones not in explorados:
                explorados.add(conexiones)
                camino[act]["conexiones"].append(conexiones)
                if conexiones != final and int(datos[conexiones]['valor_heuristico']) < int(costo_actual):
                    siguiente_nodo = conexiones
                    break
                elif conexiones == final:
                    siguiente_nodo = conexiones
                    break
        if siguiente_nodo is None:
            finalEstadistica = False
            print("Hay un mínimo local en:", act)
            colores_nodo[act] = 'red'
            break
            # Si encontramos un nodo con un costo menor, avanzamos hacia ese nodo
        else:
            act = siguiente_nodo
            print("El nuevo nodo actual es", act)

            agregar_datos_al_camino(algoritmoSeleccionado, act, estadisticas) 
            estadisticas[2][algoritmoSeleccionado] = estadisticas[2][algoritmoSeleccionado] + 1  
    print("Fin del bucle")

    if finalEstadistica:
        estadisticas[0][algoritmoSeleccionado] = 'Sí'
    else:
        estadisticas[0][algoritmoSeleccionado] = 'No'

def maximaPendiente(datos, inicial, final, camino, estadisticas, algoritmoSeleccionado):
    finalEstadistica = True
    explorados = set()
    act = inicial
    agregar_datos_al_camino(algoritmoSeleccionado, inicial, estadisticas)
    siguiente_nodo = None
    colores_nodo = {inicial: 'green', final: 'orange'}
    print("Algoritmo seleccionado: Maxima Pendiente")

    while act != final:
        if act == final:
            break
        explorados.add(act)
        camino[act] = {"conexiones": []}
        costo_actual = datos[act]['valor_heuristico']
        conexiones = datos[act]['conexiones']
        if isinstance(conexiones, str):
            conexiones = conexiones.split(', ')
        siguiente_nodo = None
        for conexion in conexiones:
            if conexion not in explorados:
                explorados.add(conexion)
                camino[act]["conexiones"].append(conexion)
                if conexion != final and int(datos[conexion]['valor_heuristico']) < int(costo_actual):
                    siguiente_nodo = conexion
                    costo_actual = datos[siguiente_nodo]['valor_heuristico']
                elif conexion == final:
                    siguiente_nodo = conexion
                    break
        if siguiente_nodo is None:
            finalEstadistica = False   #variable para ver si se llego al final
            print("Hay un mínimo local en:", act)
            colores_nodo[act] = 'red'
            break
        else:
            act = siguiente_nodo
            print("El nuevo nodo actual es", act)

            agregar_datos_al_camino(algoritmoSeleccionado, act, estadisticas) 
            estadisticas[2][algoritmoSeleccionado] = estadisticas[2][algoritmoSeleccionado] + 1  
    print("Fin del bucle")

    if finalEstadistica:
        estadisticas[0][algoritmoSeleccionado] = 'Sí'
    else:
        estadisticas[0][algoritmoSeleccionado] = 'No'
