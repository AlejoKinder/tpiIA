import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QScrollArea, QHBoxLayout, QPushButton, QCheckBox, QFrame, QComboBox, QLabel
from PyQt5.QtGui import QIntValidator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscador automático")
        self.setGeometry(100, 100, 600, 400)

        # Create a main widget to hold the entire layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a vertical layout for the main widget
        main_layout = QVBoxLayout(main_widget)

        # Create a horizontal layout for the title and "Aleatorio" button
        self.title_layout = QHBoxLayout()

        # Create a label for the title "Ingresar coordenadas"
        self.title_label = QLabel("Crear nodos")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Add the title label to the title layout
        self.title_layout.addWidget(self.title_label)

        # Create the "Aleatorio" button
        self.aleatorio_button = QPushButton("Aleatorio")
        self.aleatorio_button.clicked.connect(self.fill_random_numbers)

        # Add the "Aleatorio" button to the title layout
        self.title_layout.addWidget(self.aleatorio_button)

        # Add the title layout to the main layout
        main_layout.addLayout(self.title_layout)

        # Create a scroll area to hold the dynamic blocks
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its content
        main_layout.addWidget(self.scroll_area)

        # Create a widget to hold the dynamic blocks layout
        self.content_widget = QWidget()  # Keep a reference to the content widget
        self.scroll_area.setWidget(self.content_widget)

        self.layout = QVBoxLayout(self.content_widget)

        # Dictionary to store coordinates and connections for each label
        self.data = {}

        # Create a bottom widget to hold the buttons and checklist
        self.bottom_widget = QWidget()
        self.bottom_layout = QHBoxLayout(self.bottom_widget)

        # Add Block button
        self.add_block_button = QPushButton("Añadir nodo")
        self.add_block_button.clicked.connect(self.add_block)
        self.bottom_layout.addWidget(self.add_block_button)

        # Aceptar button
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.setEnabled(False)  # Initially disable the button
        self.accept_button.clicked.connect(self.accept_coordinates)  # Connect the method
        self.bottom_layout.addWidget(self.accept_button)

        # Add the bottom widget to the main layout
        main_layout.addWidget(self.bottom_widget)

        # Add initial block (after buttons creation)
        self.add_block()

    def add_block(self):
        # Create a block widget
        block_widget = QWidget()
        block_widget.setProperty("etiqueta", "coordenadas")
        block_widget.setStyleSheet("background-color: lightblue;")

        # Create input fields for identifier, X and Y coordinates
        identifier_edit = QLineEdit("", block_widget)
        x_coord_edit = QLineEdit("", block_widget)
        y_coord_edit = QLineEdit("", block_widget)
        valor_heuristico_edit = QLineEdit("", block_widget)

        # Set maximum length for identifier field
        identifier_edit.setMaxLength(10)

        # Apply integer validator to coordinate and heuristic value fields
        int_validator = QIntValidator()
        x_coord_edit.setValidator(int_validator)
        y_coord_edit.setValidator(int_validator)
        valor_heuristico_edit.setValidator(int_validator)

        # Create labels indicating what should go in each field
        identifier_label = QLabel("Nombre:", block_widget)
        x_coord_label = QLabel("X:", block_widget)
        y_coord_label = QLabel("Y:", block_widget)
        valor_heuristico_label = QLabel("Valor Heurístico:", block_widget)

        # Connect textChanged signal of input fields to update button state
        identifier_edit.textChanged.connect(self.habilitar_aceptar_coord)
        x_coord_edit.textChanged.connect(self.habilitar_aceptar_coord)
        y_coord_edit.textChanged.connect(self.habilitar_aceptar_coord)
        valor_heuristico_edit.textChanged.connect(self.habilitar_aceptar_coord)

        # Create separators between label and input fields
        x_separator = QFrame(block_widget)
        x_separator.setFrameShape(QFrame.VLine)
        x_separator.setFrameShadow(QFrame.Sunken)
        x_separator.setStyleSheet("background-color: blue;")
        y_separator = QFrame(block_widget)
        y_separator.setFrameShape(QFrame.VLine)
        y_separator.setFrameShadow(QFrame.Sunken)
        y_separator.setStyleSheet("background-color: blue;")
        valor_separator = QFrame(block_widget)
        valor_separator.setFrameShape(QFrame.VLine)
        valor_separator.setFrameShadow(QFrame.Sunken)
        valor_separator.setStyleSheet("background-color: blue;")

        # Arrange the label, coordinate inputs, and connection input horizontally
        hbox = QHBoxLayout()
        hbox.addWidget(identifier_label)
        hbox.addWidget(identifier_edit)
        hbox.addWidget(x_separator)  # Separator after identifier field
        hbox.addWidget(x_coord_label)
        hbox.addWidget(x_coord_edit)
        hbox.addWidget(y_separator)  # Separator after X coordinate field
        hbox.addWidget(y_coord_label)
        hbox.addWidget(y_coord_edit)
        hbox.addWidget(valor_separator)  # Separator after Y coordinate field
        hbox.addWidget(valor_heuristico_label)
        hbox.addWidget(valor_heuristico_edit)

        # Set the block's layout
        block_widget.setLayout(hbox)

        # Add the block widget to the main layout
        self.layout.addWidget(block_widget)

        # Store references to input fields in the data dictionary
        self.data[identifier_edit] = {
            'x_coord': x_coord_edit,
            'y_coord': y_coord_edit,
            'valor_heuristico': valor_heuristico_edit
        }

        # Update button state after adding a new block
        self.habilitar_aceptar_coord()

    def habilitar_aceptar_coord(self):
        # Check if any input field is empty
        for item in self.data.values():
            if item['x_coord'].text() == "" or item['y_coord'].text() == "" or item['valor_heuristico'].text() == "":
                self.accept_button.setEnabled(False)
                return
        
        # Enable the button if all input fields are filled
        self.accept_button.setEnabled(True)

    def accept_coordinates(self):
        # Clear existing content of the content widget
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.hide()

        self.title_label.setText("Asignar conexiones")
        
        # Add checklist for each block label
        for identifier_edit, attributes in self.data.items():
            block_widget = QWidget()
            block_layout = QVBoxLayout(block_widget)
            block_label = QLabel(f"Conexiones para {identifier_edit.text()}", block_widget)
            block_layout.addWidget(block_label)
            connections = []
            for other_identifier_edit in self.data.keys():
                if other_identifier_edit != identifier_edit:
                    checkbox = QCheckBox(other_identifier_edit.text(), block_widget)
                    block_layout.addWidget(checkbox)
                    connections.append(checkbox)
            attributes['connections'] = connections
            self.layout.addWidget(block_widget)

        # Delete the "Add block" button
        self.add_block_button.hide()

        # Delete the "Add block" button
        self.accept_button.hide()

        # Cambiar el funcionamiento de "Aleatorio" para que rellene las checklists
        self.aleatorio_button.clicked.disconnect(self.fill_random_numbers)
        self.aleatorio_button.clicked.connect(self.fill_random_checkboxes)

        # Create dropdown lists for selecting "Nodo inicial" and "Nodo final"
        self.initial_node_dropdown = QComboBox()  # Create the initial_node_dropdown
        self.initial_node_dropdown.addItems([identifier_edit.text() for identifier_edit in self.data.keys()])

        self.final_node_dropdown = QComboBox()  # Create the final_node_dropdown
        self.final_node_dropdown.addItems([identifier_edit.text() for identifier_edit in self.data.keys()])

        initial_label = QLabel("Nodo inicial:", block_widget)
        final_label = QLabel("Nodo final:", block_widget)
        
        self.inicial_final_widget = QWidget()
        self.inicial_final_layout = QVBoxLayout(self.inicial_final_widget)

        self.inicial_final_layout.addWidget(initial_label)
        self.inicial_final_layout.addWidget(self.initial_node_dropdown)
        self.inicial_final_layout.addWidget(final_label)
        self.inicial_final_layout.addWidget(self.final_node_dropdown)

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
        
        self.bottom_layout.addWidget(self.inicial_final_widget)
        self.bottom_layout.addWidget(self.busq_y_nav)

    def fill_random_numbers(self):
        # Fill input fields with random numbers from 0 to 30, ensuring unique coordinates
        used_coordinates = set()  # Set to store used coordinates
        for attributes in self.data.values():
            valor_heuristico = random.randint(0, 100)
            x_coord = random.randint(0, 30)
            y_coord = random.randint(0, 30)
            while (x_coord, y_coord) in used_coordinates:
                x_coord = random.randint(0, 30)
                y_coord = random.randint(0, 30)
            used_coordinates.add((x_coord, y_coord))
            attributes['x_coord'].setText(str(x_coord))
            attributes['y_coord'].setText(str(y_coord))
            attributes['valor_heuristico'].setText(str(valor_heuristico))

        for i, (identifier_edit, attributes) in enumerate(self.data.items()):
            identifier = chr(ord('A') + i)  # Convert index to corresponding character (A-Z)
            identifier_edit.setText(identifier)

    def fill_random_checkboxes(self):
        # Create a dictionary to store bidirectional connections
        bidirectional_connections = {}

        # Initialize bidirectional connections for each block
        for identifier_edit in self.data.keys():
            bidirectional_connections[identifier_edit.text()] = set()

        # Fill checkboxes randomly for each block
        for identifier_edit, attributes in self.data.items():
            connections = attributes['connections']
            for checkbox in connections:
                # Randomly select whether to check the checkbox
                checkbox.setChecked(bool(random.getrandbits(1)))
                
                # If the checkbox is checked, establish bidirectional connection
                if checkbox.isChecked():
                    other_identifier = checkbox.text()
                    # Add bidirectional connection
                    bidirectional_connections[identifier_edit.text()].add(other_identifier)
                    bidirectional_connections[other_identifier].add(identifier_edit.text())

        # Apply bidirectional connections to all blocks
        for identifier_edit, attributes in self.data.items():
            connections = attributes['connections']
            for checkbox in connections:
                other_identifier = checkbox.text()
                if other_identifier in bidirectional_connections[identifier_edit.text()]:
                    checkbox.setChecked(True)

        self.initial_node_dropdown.setCurrentIndex(random.randint(0, self.initial_node_dropdown.count() - 1))
        self.final_node_dropdown.setCurrentIndex(random.randint(0, self.final_node_dropdown.count() - 1))
        
    def print_attributes(self):
        # Print the values of the attributes and connections of each label to the console
        for identifier_edit, attributes in self.data.items():
            x_coord = attributes['x_coord'].text()
            y_coord = attributes['y_coord'].text()
            valor_heuristico = attributes['valor_heuristico'].text()
            connections = [checkbox.text() for checkbox in attributes['connections'] if checkbox.isChecked()]
            print(f"Identifier: {identifier_edit.text()}, X Coord: {x_coord}, Y Coord: {y_coord}, Valor Heurístico: {valor_heuristico}, Connections: {connections}")

    def escalada_simple(self):
        self.print_attributes()
        print(f"Escalada simple")
        print(f"Nodo inicial: {self.initial_node_dropdown.currentText()}")
        print(f"Nodo final: {self.final_node_dropdown.currentText()}")


    def maxima_pendiente(self):
        self.print_attributes()
        print("Máxima pendiente")
        print(f"Nodo inicial: {self.initial_node_dropdown.currentText()}")
        print(f"Nodo final: {self.final_node_dropdown.currentText()}")

    def volver(self):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if (widget is not None and widget.property("etiqueta") != "coordenadas"):
                widget.deleteLater()

        for i in range(self.bottom_layout.count()):
            widget = self.bottom_layout.itemAt(i).widget()
            if widget is not None:
                widget.hide()

        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if (widget is not None):
                widget.show()

        self.add_block_button.show()
        self.accept_button.show()
        self.title_label.setText("Crear nodos")
        self.aleatorio_button.clicked.disconnect(self.fill_random_checkboxes)
        self.aleatorio_button.clicked.connect(self.fill_random_numbers)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()