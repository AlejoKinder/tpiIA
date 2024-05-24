import math
import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QScrollArea, QHBoxLayout, QPushButton, QCheckBox, QFrame, QComboBox, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIntValidator

import algoritmo   #archivo que hace los algoritmos
import resultados   #archivo que muestra la tabla de resultados

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscador automático")
        self.setGeometry(100, 100, 500, 400)

        self.resultados_mostrados = False

        self.widget_principal = QWidget()
        self.setCentralWidget(self.widget_principal)

        self.layout_principal_h = QHBoxLayout(self.widget_principal)
        widget_principal_v = QWidget()
        layout_principal_v = QVBoxLayout(widget_principal_v)
        self.layout_principal_h.addWidget(widget_principal_v)

        self.titulo_layout = QHBoxLayout()

        self.label_titulo = QLabel("Crear nodos")
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.titulo_layout.addWidget(self.label_titulo)

        self.boton_aleatorio = QPushButton("Aleatorio")
        self.boton_aleatorio.clicked.connect(self.aleatorio_numeros)

        self.titulo_layout.addWidget(self.boton_aleatorio)

        layout_principal_v.addLayout(self.titulo_layout)


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  
        layout_principal_v.addWidget(self.scroll_area)

        # Crear widget para contener los bloques de los nodos
        self.widget_nodos = QWidget()
        self.scroll_area.setWidget(self.widget_nodos)

        self.layout_scroll = QVBoxLayout(self.widget_nodos)

        # Diccionario para guardar todos los datos de los nodos
        self.datos_nodos = {}

        # Widget de botones de "aceptar" y "añadir nodo"
        self.widget_inferior = QWidget()
        self.layout_inferior = QHBoxLayout(self.widget_inferior)


        self.boton_aniadir_nodo = QPushButton("Añadir nodo")
        self.boton_aniadir_nodo.clicked.connect(self.aniadir_nodo)
        self.layout_inferior.addWidget(self.boton_aniadir_nodo)


        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.setEnabled(False)  # Deshabilitar el botón al inicio, para requerir que el usuario rellene los campos
        self.boton_aceptar.clicked.connect(self.aceptar_nodos)  # Método del botón
        self.layout_inferior.addWidget(self.boton_aceptar)

 
        layout_principal_v.addWidget(self.widget_inferior)

        # Añadir el primer nodo
        self.aniadir_nodo()

    def aniadir_nodo(self):
        widget_nodo = QWidget()
        widget_nodo.setProperty("etiqueta", "coordenadas")
        widget_nodo.setStyleSheet("background-color: lightblue;")

        # Se crean campos de propiedades del nodo
        LEdit_nombre = QLineEdit("", widget_nodo)
        LEdit_coord_x = QLineEdit("", widget_nodo)
        LEdit_coord_y = QLineEdit("", widget_nodo)

        LEdit_nombre.setMaxLength(20)

        # Se añade un validador para que no se puedan ingresar letras en campos donde van números
        validador = QIntValidator()
        LEdit_coord_x.setValidator(validador)
        LEdit_coord_y.setValidator(validador)

        label_nombre = QLabel("Nombre:", widget_nodo)
        label_coord_x = QLabel("X:", widget_nodo)
        label_coord_y = QLabel("Y:", widget_nodo)

        # Se verifica si se debe habilitar el botón "aceptar" cuando ocurre un cambio en algún campo
        LEdit_nombre.textChanged.connect(self.habilitar_boton_aceptar)
        LEdit_coord_x.textChanged.connect(self.habilitar_boton_aceptar)
        LEdit_coord_y.textChanged.connect(self.habilitar_boton_aceptar)

        # Separadores (estético)
        separador_x = QFrame(widget_nodo)
        separador_x.setFrameShape(QFrame.VLine)
        separador_x.setFrameShadow(QFrame.Sunken)
        separador_x.setStyleSheet("background-color: blue;")
        separador_y = QFrame(widget_nodo)
        separador_y.setFrameShape(QFrame.VLine)
        separador_y.setFrameShadow(QFrame.Sunken)
        separador_y.setStyleSheet("background-color: blue;")

        # Combinación de los campos y separadores
        hbox = QHBoxLayout()
        hbox.addWidget(label_nombre)
        hbox.addWidget(LEdit_nombre)
        hbox.addWidget(separador_x)
        hbox.addWidget(label_coord_x)
        hbox.addWidget(LEdit_coord_x)
        hbox.addWidget(separador_y)
        hbox.addWidget(label_coord_y)
        hbox.addWidget(LEdit_coord_y)

        widget_nodo.setLayout(hbox)

        self.layout_scroll.addWidget(widget_nodo)

        # Se enlazan los nodos con los campos, para que se guarden aún en la pantalla siguiente, para poder volver hacia atrás
        self.datos_nodos[LEdit_nombre] = {
            'coord_x': LEdit_coord_x,
            'coord_y': LEdit_coord_y,
        }

        # Se deshabilita el botón de aceptar al añadir un nuevo bloque
        self.habilitar_boton_aceptar()

    def habilitar_boton_aceptar(self):
        # Verificar si hay algún campo vacío
        for nodo, atributos in self.datos_nodos.items():
            if nodo.text() == "" or atributos['coord_x'].text() == "" or atributos['coord_y'].text() == "":
                self.boton_aceptar.setEnabled(False)
                return
        
        # Habilitar el botón si no hay ningún campo vacío
        self.boton_aceptar.setEnabled(True)

    def aceptar_nodos(self):
        # Se esconden los bloques de los nodos
        for i in reversed(range(self.layout_scroll.count())):
            widget = self.layout_scroll.itemAt(i).widget()
            if widget is not None:
                widget.hide()

        # Crear el área para mostrar los valores heurísticos
        self.separador_heuristica = QFrame()
        self.separador_heuristica.setFrameShape(QFrame.VLine)
        self.separador_heuristica.setFrameShadow(QFrame.Sunken)
        self.layout_principal_h.addWidget(self.separador_heuristica)

        self.widget_heuristicas = QWidget()
        layout_heuristicas = QVBoxLayout(self.widget_heuristicas)
        label_heuristicas = QLabel("Valores heurísticos", self.widget_heuristicas)
        layout_heuristicas.addWidget(label_heuristicas)
        label_heuristicas.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.scroll_heuristicas = QScrollArea()
        self.scroll_heuristicas.setWidgetResizable(True)
        self.scroll_heuristicas.setMinimumWidth(220)
        layout_heuristicas.addWidget(self.scroll_heuristicas)
        self.layout_principal_h.addWidget(self.widget_heuristicas)
        
        self.label_titulo.setText("Asignar conexiones")
        
        # Se crean checklists por cada nodo ingresado
        for nombre, atributos in self.datos_nodos.items():
            widget = QWidget()
            layout = QVBoxLayout(widget)
            etiqueta = QLabel(f"Conexiones para {nombre.text()}", widget)
            layout.addWidget(etiqueta)
            conexiones = []
            for otro_nombre in self.datos_nodos.keys():
                if otro_nombre != nombre:
                    checkbox = QCheckBox(otro_nombre.text(), widget)
                    checkbox.stateChanged.connect(self.asegurar_bidireccionalidad)
                    layout.addWidget(checkbox)
                    conexiones.append(checkbox)
            atributos['conexiones'] = conexiones
            self.layout_scroll.addWidget(widget)

        # Se esconden también los bloques de "añadir nodo" y "aceptar"
        self.boton_aniadir_nodo.hide()
        self.boton_aceptar.hide()

        # Cambiar el funcionamiento de "Aleatorio" para que rellene las checklists
        self.boton_aleatorio.clicked.disconnect(self.aleatorio_numeros)
        self.boton_aleatorio.clicked.connect(self.aleatorio_checkboxes)

        # Creación combobox para nodos inicial y final
        self.nodo_inicial = QComboBox()  
        self.nodo_inicial.addItems([nombre_nodo.text() for nombre_nodo in self.datos_nodos.keys()])

        self.nodo_final = QComboBox()  
        self.nodo_final.addItems([nombre_nodo.text() for nombre_nodo in self.datos_nodos.keys()])

        label_inicial = QLabel("Nodo inicial:", widget)
        label_final = QLabel("Nodo final:", widget)
        
        self.inicial_final_widget = QWidget()
        self.inicial_final_layout = QVBoxLayout(self.inicial_final_widget)

        self.inicial_final_layout.addWidget(label_inicial)
        self.inicial_final_layout.addWidget(self.nodo_inicial)
        self.inicial_final_layout.addWidget(label_final)
        self.inicial_final_layout.addWidget(self.nodo_final)

        self.busq_y_nav = QWidget()
        self.busq_y_nav_layout = QVBoxLayout(self.busq_y_nav)

        self.metodo_busqueda_widget = QWidget()
        self.metodo_busqueda_layout = QHBoxLayout(self.metodo_busqueda_widget)

        self.boton_busqueda_euclidea = QPushButton("Distancia euclídea")
        self.boton_busqueda_euclidea.clicked.connect(self.busqueda_euclidea)
        self.metodo_busqueda_layout.addWidget(self.boton_busqueda_euclidea)
        
        self.boton_busqueda_manhattan = QPushButton("Distancia Manhattan")
        self.boton_busqueda_manhattan.clicked.connect(self.busqueda_manhattan)
        self.metodo_busqueda_layout.addWidget(self.boton_busqueda_manhattan)

        self.metodo_busqueda_layout.setContentsMargins(0, 0, 0, 20)

        self.label_busqueda = QLabel("Elegir heurística:")

        self.busq_y_nav_layout.addWidget(self.label_busqueda)
        self.busq_y_nav_layout.addWidget(self.metodo_busqueda_widget)

        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volver)
        self.busq_y_nav_layout.addWidget(self.boton_volver)
        
        self.layout_inferior.addWidget(self.inicial_final_widget)
        self.layout_inferior.addWidget(self.busq_y_nav)

    def asegurar_bidireccionalidad(self, estado):
        checkbox_clickeada = self.sender()
        for nodo, atributos in self.datos_nodos.items():
            if checkbox_clickeada in atributos['conexiones']:
                nodo_clickeado = nodo
        for nodo in self.datos_nodos.keys():
            if nodo.text() == checkbox_clickeada.text():
                for conexion_checkbox in self.datos_nodos[nodo]['conexiones']:
                    if conexion_checkbox.text() == nodo_clickeado.text():
                        if estado == 2:
                            conexion_checkbox.setChecked(True)
                        else:
                            conexion_checkbox.setChecked(False)


    def aleatorio_numeros(self):
        # Rellenar las coordenadas con números aleatorios únicos
        coordenadas_existentes = set()
        for atributos in self.datos_nodos.values():
            coord_x = random.randint(0, 30)
            coord_y = random.randint(0, 30)
            while (coord_x, coord_y) in coordenadas_existentes:
                coord_x = random.randint(0, 30)
                coord_y = random.randint(0, 30)
            coordenadas_existentes.add((coord_x, coord_y))
            atributos['coord_x'].setText(str(coord_x))
            atributos['coord_y'].setText(str(coord_y))

        # Rellenar nombres de nodos de la A a la Z
        for i, (nombre_nodo, atributos) in enumerate(self.datos_nodos.items()):
            letra = chr(ord('A') + i) 
            nombre_nodo.setText(letra)

    def aleatorio_checkboxes(self):
        # Se rellenan aleatoriamente las checkboxes
        for atributos in self.datos_nodos.values():
            conexiones = atributos['conexiones']
            for checkbox in conexiones:
                checkbox.setChecked(bool(random.getrandbits(1)))

        # También se selecciona un valor aleatorio para nodo inicial y final
        self.nodo_inicial.setCurrentIndex(random.randint(0, self.nodo_inicial.count() - 1))
        self.nodo_final.setCurrentIndex(random.randint(0, self.nodo_final.count() - 1))
        
    def imprimir_atributos(self, diccionario):
        # Se imprimen los atributos
        for nodo, atributos in diccionario.items():
            print(f"Nombre: {nodo}, Coord X: {atributos['coord_x']}, Coord Y: {atributos['coord_y']}, Valor Heurístico: {atributos['valor_heuristico']}, conexiones: {atributos['conexiones']}")

    def busqueda_euclidea(self):
        print(f"Búsqueda con heurística por distancia euclídea")
        print(f"Nodo inicial: {self.nodo_inicial.currentText()}")
        print(f"Nodo final: {self.nodo_final.currentText()}")

        self.boton_busqueda_manhattan.setEnabled(False)
        self.boton_busqueda_euclidea.setEnabled(False)
        self.boton_volver.setEnabled(False)

        if(self.resultados_mostrados):
            self.tabla.close()

        diccionario_busqueda = self.calcular_heuristicas(0)
        self.imprimir_atributos(diccionario_busqueda)

        estadisticas = algoritmo.ejecutar_algoritmos(diccionario_busqueda, self.nodo_inicial.currentText(), self.nodo_final.currentText())

        self.tabla = resultados.PopupResultados(0, estadisticas)
        self.tabla.show()
        self.resultados_mostrados = True
        self.boton_busqueda_manhattan.setEnabled(True)
        self.boton_busqueda_euclidea.setEnabled(True)
        self.boton_volver.setEnabled(True)

    def busqueda_manhattan(self):
        print("Búsqueda con heurística por distancia Manhattan")
        print(f"Nodo inicial: {self.nodo_inicial.currentText()}")
        print(f"Nodo final: {self.nodo_final.currentText()}")

        self.boton_busqueda_manhattan.setEnabled(False)
        self.boton_busqueda_euclidea.setEnabled(False)
        self.boton_volver.setEnabled(False)

        if(self.resultados_mostrados):
            self.tabla.close()

        diccionario_busqueda = self.calcular_heuristicas(1)

        self.imprimir_atributos(diccionario_busqueda)

        estadisticas = algoritmo.ejecutar_algoritmos(diccionario_busqueda, self.nodo_inicial.currentText(), self.nodo_final.currentText())

        self.tabla = resultados.PopupResultados(1, estadisticas)
        self.tabla.show()
        self.resultados_mostrados = True
        self.boton_busqueda_manhattan.setEnabled(True)
        self.boton_busqueda_euclidea.setEnabled(True)
        self.boton_volver.setEnabled(True)
        

    def calcular_heuristicas(self, heuristica):
        # Calcular valores heurísticos y transformar los datos del diccionario para poder realizar búsquedas
        nodo_final = self.nodo_final.currentText()
        for nodo in self.datos_nodos.keys():
            if nodo.text() == nodo_final:
                nodo_final = nodo
        nodo_final_coord_x = int(self.datos_nodos[nodo_final]['coord_x'].text())
        nodo_final_coord_y = int(self.datos_nodos[nodo_final]['coord_y'].text())
        
        diccionario_busqueda = {}  # Nuevo diccionario
        for nodo, atributos in self.datos_nodos.items():
            if(heuristica == 0):
                valor_heuristico = math.sqrt((nodo_final_coord_x - int(atributos['coord_x'].text()))**2 + (nodo_final_coord_y - int(atributos['coord_y'].text()))**2)
            else:
                valor_heuristico = abs(int(atributos['coord_x'].text()) - nodo_final_coord_x) + abs(int(atributos['coord_y'].text()) - nodo_final_coord_y)
            nuevo_nodo = str(nodo.text())
            nuevas_conexiones = [checkbox.text() for checkbox in atributos['conexiones'] if checkbox.isChecked()]
            nuevos_atributos = {
                'coord_x': str(atributos['coord_x'].text()),
                'coord_y': str(atributos['coord_y'].text()),
                'valor_heuristico': round(valor_heuristico),
                'conexiones': nuevas_conexiones
            }
            diccionario_busqueda[nuevo_nodo] = nuevos_atributos
        
        tabla_heuristicas = QTableWidget()
        tabla_heuristicas.setColumnCount(2)  # Set the number of columns
        tabla_heuristicas.setRowCount(len(diccionario_busqueda))
        tabla_heuristicas.setHorizontalHeaderLabels(["Nodo", "Valor heurístico"])
        tabla_heuristicas.horizontalHeader().setMinimumSectionSize(100)

        i = 0
        j = 0
        for key, datos in diccionario_busqueda.items():
            item = QTableWidgetItem(key)
            tabla_heuristicas.setItem(i, j, item)
            j += 1
            item = QTableWidgetItem(str(datos['valor_heuristico']))
            tabla_heuristicas.setItem(i, j, item)
            i += 1
            j = 0
            
        self.scroll_heuristicas.setWidget(tabla_heuristicas)
        
        return diccionario_busqueda

    def volver(self):
        # Borrar los datos de la pantalla de conexiones
        for i in range(self.layout_scroll.count()):
            widget = self.layout_scroll.itemAt(i).widget()
            if (widget is not None and widget.property("etiqueta") != "coordenadas"):
                widget.deleteLater()

        self.widget_heuristicas.deleteLater()

        self.separador_heuristica.deleteLater()

        # Esconder los elementos del widget inferior
        for i in range(self.layout_inferior.count()):
            widget = self.layout_inferior.itemAt(i).widget()
            if widget is not None:
                widget.hide()

        # Volver a mostrar los datos de la pantalla anterior
        for i in range(self.layout_scroll.count()):
            widget = self.layout_scroll.itemAt(i).widget()
            if (widget is not None):
                widget.show()

        self.boton_aniadir_nodo.show()
        self.boton_aceptar.show()
        self.label_titulo.setText("Crear nodos")
        self.boton_aleatorio.clicked.disconnect(self.aleatorio_checkboxes)
        self.boton_aleatorio.clicked.connect(self.aleatorio_numeros)

def main():
    aplicacion = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(aplicacion.exec_())

if __name__ == "__main__":
    main()
