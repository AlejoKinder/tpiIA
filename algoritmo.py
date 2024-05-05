import interfaz   # Posiblemente tengamos que hacer al revés, dijo el que se resbaló y cayó de espalda.
import random

def escaladaSimple(data):
    actual = ''
    final = 'C'   #momentaneamente la forma de saber cual es el nodo final, hasta que tute se digne a añadir cual es el final en el diccionario.
    explorados = []
    i = 0   #momentaneamente la forma de acceder a la heuristica, hasta que tute se digne a añadir el atributo para el costo de la conexion entre nodos. 

    for label_char, item in data.items():   # Iteramos sobre el diccionario
        print("Estoy en el datos:", label_char)   #depuración
        connections_str = item['connections'].text()  # Obtener la cadena de conexiones
        cant_items = cantItems(connections_str)  # Obtener la cantidad de elementos en la lista
        vectorCosto = crear_vector(cantItems)
        imprimirVector(vectorCosto)   #depuración

        for connection in connections_str.split(', '):  # Iterar sobre cada conexión
            # Realizar acciones con cada conexión
            if()

def cantItems(connections_str):
    # Dividir la cadena en una lista
    connections_list = connections_str.split(', ')
    # Obtener la cantidad de elementos en la lista
    cantidad_items = len(connections_list)
    return cantidad_items


def crear_vector(cant_items):   #esto es momentaneo hasta que tute se digne a añadir el atributo para el costo de la conexion entre nodos.
    vector = []
    for _ in range(cant_items):
        valor = random.randint(1, 50)  # Genera un valor aleatorio entre 1 y 50
        vector.append(valor)
    return vector

def imprimirVector(vector):
    # Convertir los elementos del vector en una cadena separada por espacios
    cadena_vector = ' '.join(map(str, vector))

    # Imprimir la cadena resultante
    print(cadena_vector)
