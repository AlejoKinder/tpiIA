import networkx as nx
import matplotlib.pyplot as plt

def agregarGrafo(G, u, v, w = 1, sent = True):
    G.add_edge(u, v, weight = w)

    #si sentido es falso, quiere decir que queremos que sea unidireccional
    if sent:
        G.add_edge(v, u, weight = w)
    
if __name__ == '__main__':
    #Creamos la variable que contiene el grafico.
    G = nx.DiGraph()


    #Creamos nodos
    agregarGrafo(G, "A", "B", 3)
    agregarGrafo(G, "C", "B", 1, False)

    #Creamos las conexiones
    pos = nx.layout.planar_layout(G)   #se puede cambiar planar_layaout por otros, para que dibuje de distintas formas.
    print(pos)   #imprime donde se dibujan cada uno de los grafos
    nx.draw_networkx(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')   #sirve para escribir las distancias
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Grafo con NetworkX")   
    plt.show()