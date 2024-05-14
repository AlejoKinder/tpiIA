import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QScrollArea, QHBoxLayout, QPushButton, QCheckBox, QFrame, QComboBox, QLabel
from PyQt5.QtGui import QIntValidator

import algoritmo   #archivo que hace los algoritmos

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscador automático")
        self.setGeometry(100, 100, 600, 400)

        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        layout_principal = QVBoxLayout(widget_principal)

        self.titulo_layout = QHBoxLayout()

        self.label_titulo = QLabel("Crear nodos")
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.titulo_layout.addWidget(self.label_titulo)

        self.boton_aleatorio = QPushButton("Aleatorio")
        self.boton_aleatorio.clicked.connect(self.aleatorio_numeros)

        self.titulo_layout.addWidget(self.boton_aleatorio)

        layout_principal.addLayout(self.titulo_layout)


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  
        layout_principal.addWidget(self.scroll_area)

        # Crear widget para contener los bloques de los nodos
        self.widget_nodos = QWidget()
        self.scroll_area.setWidget(self.widget_nodos)

        self.layout = QVBoxLayout(self.widget_nodos)

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

 
        layout_principal.addWidget(self.widget_inferior)

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
        LEdit_valor_heuristico = QLineEdit("", widget_nodo)

        LEdit_nombre.setMaxLength(20)

        # Se añade un validador para que no se puedan ingresar letras en campos donde van números
        validador = QIntValidator()
        LEdit_coord_x.setValidator(validador)
        LEdit_coord_y.setValidator(validador)
        LEdit_valor_heuristico.setValidator(validador)

        label_nombre = QLabel("Nombre:", widget_nodo)
        label_coord_x = QLabel("X:", widget_nodo)
        label_coord_y = QLabel("Y:", widget_nodo)
        label_valor_heuristico = QLabel("Valor Heurístico:", widget_nodo)

        # Se verifica si se debe habilitar el botón "aceptar" cuando ocurre un cambio en algún campo
        LEdit_nombre.textChanged.connect(self.habilitar_boton_aceptar)
        LEdit_coord_x.textChanged.connect(self.habilitar_boton_aceptar)
        LEdit_coord_y.textChanged.connect(self.habilitar_boton_aceptar)
        LEdit_valor_heuristico.textChanged.connect(self.habilitar_boton_aceptar)

        # Separadores (estético)
        separador_x = QFrame(widget_nodo)
        separador_x.setFrameShape(QFrame.VLine)
        separador_x.setFrameShadow(QFrame.Sunken)
        separador_x.setStyleSheet("background-color: blue;")
        separador_y = QFrame(widget_nodo)
        separador_y.setFrameShape(QFrame.VLine)
        separador_y.setFrameShadow(QFrame.Sunken)
        separador_y.setStyleSheet("background-color: blue;")
        separador_valor_heuristico = QFrame(widget_nodo)
        separador_valor_heuristico.setFrameShape(QFrame.VLine)
        separador_valor_heuristico.setFrameShadow(QFrame.Sunken)
        separador_valor_heuristico.setStyleSheet("background-color: blue;")

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
        hbox.addWidget(separador_valor_heuristico)
        hbox.addWidget(label_valor_heuristico)
        hbox.addWidget(LEdit_valor_heuristico)

        widget_nodo.setLayout(hbox)

        self.layout.addWidget(widget_nodo)

        # Se enlazan los nodos con los campos, para que se guarden aún en la pantalla siguiente, para poder volver hacia atrás
        self.datos_nodos[LEdit_nombre] = {
            'coord_x': LEdit_coord_x,
            'coord_y': LEdit_coord_y,
            'valor_heuristico': LEdit_valor_heuristico
        }

        # Se deshabilita el botón de aceptar al añadir un nuevo bloque
        self.habilitar_boton_aceptar()

    def habilitar_boton_aceptar(self):
        # Verificar si hay algún campo vacío
        for nodo, atributos in self.datos_nodos.items():
            if nodo.text() == "" or atributos['coord_x'].text() == "" or atributos['coord_y'].text() == "" or atributos['valor_heuristico'].text() == "":
                self.boton_aceptar.setEnabled(False)
                return
        
        # Habilitar el botón si no hay ningún campo vacío
        self.boton_aceptar.setEnabled(True)

    def aceptar_nodos(self):
        # Se esconden los bloques de los nodos
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.hide()

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
            self.layout.addWidget(widget)

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

        self.boton_escalada_simple = QPushButton("Escalada simple")
        self.boton_escalada_simple.clicked.connect(self.escalada_simple)
        self.metodo_busqueda_layout.addWidget(self.boton_escalada_simple)
        
        self.boton_maxima_pendiente = QPushButton("Máxima pendiente")
        self.boton_maxima_pendiente.clicked.connect(self.maxima_pendiente)
        self.metodo_busqueda_layout.addWidget(self.boton_maxima_pendiente)

        self.busq_y_nav_layout.addWidget(self.metodo_busqueda_widget)

        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volver)
        self.busq_y_nav_layout.addWidget(self.boton_volver)
        
        self.layout_inferior.addWidget(self.inicial_final_widget)
        self.layout_inferior.addWidget(self.busq_y_nav)

    def asegurar_bidireccionalidad(self, estado):
        if estado == 2:
            checkbox_clickeada = self.sender()
            for nodo, atributos in self.datos_nodos.items():
                if checkbox_clickeada in atributos['conexiones']:
                    nodo_clickeado = nodo
            for nodo in self.datos_nodos.keys():
                if nodo.text() == checkbox_clickeada.text():
                    for conexion_checkbox in self.datos_nodos[nodo]['conexiones']:
                        if conexion_checkbox.text() == nodo_clickeado.text():
                            conexion_checkbox.setChecked(True)
        else:
            checkbox_clickeada = self.sender()
            for nodo, atributos in self.datos_nodos.items():
                if checkbox_clickeada in atributos['conexiones']:
                    nodo_clickeado = nodo
            for nodo in self.datos_nodos.keys():
                if nodo.text() == checkbox_clickeada.text():
                    for conexion_checkbox in self.datos_nodos[nodo]['conexiones']:
                        if conexion_checkbox.text() == nodo_clickeado.text():
                            conexion_checkbox.setChecked(False)


    def aleatorio_numeros(self):
        # Rellenar las coordenadas con números aleatorios únicos
        coordenadas_existentes = set()
        for atributos in self.datos_nodos.values():
            valor_heuristico = random.randint(0, 100)
            coord_x = random.randint(0, 30)
            coord_y = random.randint(0, 30)
            while (coord_x, coord_y) in coordenadas_existentes:
                coord_x = random.randint(0, 30)
                coord_y = random.randint(0, 30)
            coordenadas_existentes.add((coord_x, coord_y))
            atributos['coord_x'].setText(str(coord_x))
            atributos['coord_y'].setText(str(coord_y))
            atributos['valor_heuristico'].setText(str(valor_heuristico))

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
        
    def imprimir_atributos(self):
        # Se imprimen los atributos
        for nodo, atributos in self.datos_nodos.items():
            coord_x = atributos['coord_x'].text()
            coord_y = atributos['coord_y'].text()
            valor_heuristico = atributos['valor_heuristico'].text()
            conexiones = [checkbox.text() for checkbox in atributos['conexiones'] if checkbox.isChecked()]
            print(f"Identifier: {nodo.text()}, X Coord: {coord_x}, Y Coord: {coord_y}, Valor Heurístico: {valor_heuristico}, conexiones: {conexiones}")

    def escalada_simple(self):
        self.imprimir_atributos()
        print(f"Escalada simple")
        print(f"Nodo inicial: {self.nodo_inicial.currentText()}")
        print(f"Nodo final: {self.nodo_final.currentText()}")

        diccionario_transformado = self.transformar_diccionario()

        algoritmo.escaladaSimple(diccionario_transformado, self.nodo_inicial.currentText(), self.nodo_final.currentText())

    def maxima_pendiente(self):
        self.imprimir_atributos()
        print("Máxima pendiente")
        print(f"Nodo inicial: {self.nodo_inicial.currentText()}")
        print(f"Nodo final: {self.nodo_final.currentText()}")

        diccionario_transformado = self.transformar_diccionario()

        algoritmo.maximaPendiente(diccionario_transformado, self.nodo_inicial.currentText(), self.nodo_final.currentText())

    def transformar_diccionario(self):
        # Transformar los datos del diccionario a STRING, para poder realizar búsquedas
        diccionario_transformado = {}  # Nuevo diccionario con STRINGS
        for nodo, atributos in self.datos_nodos.items():
            nuevo_nodo = str(nodo.text())
            nuevas_conexiones = [checkbox.text() for checkbox in atributos['conexiones'] if checkbox.isChecked()]
            nuevos_atributos = {
                'coord_x': str(atributos['coord_x'].text()),
                'coord_y': str(atributos['coord_y'].text()),
                'valor_heuristico': str(atributos['valor_heuristico'].text()),
                'conexiones': nuevas_conexiones
            }
            diccionario_transformado[nuevo_nodo] = nuevos_atributos
        return diccionario_transformado

    def volver(self):
        # Borrar los datos de la pantalla de conexiones
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if (widget is not None and widget.property("etiqueta") != "coordenadas"):
                widget.deleteLater()

        # Esconder los elementos del widget inferior
        for i in range(self.layout_inferior.count()):
            widget = self.layout_inferior.itemAt(i).widget()
            if widget is not None:
                widget.hide()

        # Volver a mostrar los datos de la pantalla anterior
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if (widget is not None):
                widget.show()

        self.boton_aniadir_nodo.show()
        self.boton_aceptar.show()
        self.label_titulo.setText("Crear nodos")
        self.boton_aleatorio.clicked.disconnect(self.aleatorio_checkboxes)
        self.boton_aleatorio.clicked.connect(self.aleatorio_numeros)

def main():
    aplicación = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(aplicación.exec_())

if __name__ == "__main__":
    main()
