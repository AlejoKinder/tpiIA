import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QScrollArea, QHBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynamic Block Example")
        self.setGeometry(100, 100, 600, 400)

        # Create a main widget to hold the entire layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a vertical layout for the main widget
        main_layout = QVBoxLayout(main_widget)

        # Create a horizontal layout for the title and "Aleatorio" button
        title_layout = QHBoxLayout()

        # Create a label for the title "Ingresar coordenadas"
        title_label = QLabel("Ingresar coordenadas")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Add the title label to the title layout
        title_layout.addWidget(title_label)

        # Create the "Aleatorio" button
        self.aleatorio_button = QPushButton("Aleatorio")
        self.aleatorio_button.clicked.connect(self.fill_random_numbers)

        # Add the "Aleatorio" button to the title layout
        title_layout.addWidget(self.aleatorio_button)

        # Add the title layout to the main layout
        main_layout.addLayout(title_layout)

        # Create a scroll area to hold the dynamic blocks
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its content
        main_layout.addWidget(self.scroll_area)

        # Create a widget to hold the dynamic blocks layout
        self.content_widget = QWidget()  # Keep a reference to the content widget
        self.scroll_area.setWidget(self.content_widget)

        self.layout = QVBoxLayout(self.content_widget)

        # Initialize label index for blocks starting from 'A'
        self.label_index = 0

        # Dictionary to store coordinates and connections for each label
        self.data = {}

        # Create a bottom widget to hold the buttons
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        
        # Add Block button
        self.add_block_button = QPushButton("Add Block")
        self.add_block_button.clicked.connect(self.add_block)
        bottom_layout.addWidget(self.add_block_button)

        # Aceptar button
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.setEnabled(False)  # Initially disable the button
        self.accept_button.clicked.connect(self.accept_coordinates)  # Connect the method
        bottom_layout.addWidget(self.accept_button)

        # Add the bottom widget to the main layout
        main_layout.addWidget(bottom_widget)

        # Add initial block (after buttons creation)
        self.add_block()

    def add_block(self):
        # Check if the label index has reached 'Z'
        if self.label_index == 26:
            self.add_block_button.setEnabled(False)  # Disable button if limit is reached
            return

        # Create a block widget
        block_widget = QWidget()
        block_widget.setStyleSheet("background-color: lightblue;")

        # Create a label from 'A' onwards
        label_char = chr(ord('A') + self.label_index)
        label = QLabel(label_char, block_widget)
        label.setStyleSheet("font-weight: bold; font-size: 16px;")

        # Increment label index for the next block
        self.label_index += 1

        # Create input fields for X and Y coordinates
        x_coord_edit = QLineEdit("", block_widget)
        y_coord_edit = QLineEdit("", block_widget)
        connection_edit = QLineEdit("", block_widget)  # Input field for connections

        # Connect textChanged signal of input fields to update button state
        x_coord_edit.textChanged.connect(self.update_button_state)
        y_coord_edit.textChanged.connect(self.update_button_state)
        connection_edit.textChanged.connect(self.update_button_state)

        # Arrange the label, coordinate inputs, and connection input horizontally
        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(x_coord_edit)
        hbox.addWidget(y_coord_edit)
        hbox.addWidget(connection_edit)  # Add connection input field

        # Set the block's layout
        block_widget.setLayout(hbox)

        # Add the block widget to the main layout
        self.layout.addWidget(block_widget)

        # Store coordinates and connections in the data dictionary
        self.data[label_char] = {
            'x_coord': x_coord_edit,
            'y_coord': y_coord_edit,
            'connections': connection_edit
        }

        # Disable Add Block button if 'Z' block is created
        if self.label_index == 26:
            self.add_block_button.setEnabled(False)

        # Update button state after adding a new block
        self.update_button_state()

    def update_button_state(self):
        # Check if any input field is empty
        for item in self.data.values():
            if item['x_coord'].text() == "" or item['y_coord'].text() == "" or item['connections'].text() == "":
                self.accept_button.setEnabled(False)
                return
        
        # Enable the button if all input fields are filled
        self.accept_button.setEnabled(True)

    def accept_coordinates(self):
        # Print the coordinates and connections (for demonstration purposes)
        for label_char, item in self.data.items():
            x_coord = item['x_coord'].text()
            y_coord = item['y_coord'].text()
            connections = item['connections'].text()
            print(f"Label: {label_char}, X: {x_coord}, Y: {y_coord}, Connections: {connections}")

    def fill_random_numbers(self):
        # Fill input fields with random numbers from 0 to 30, ensuring unique coordinates
        used_coordinates = set()  # Set to store used coordinates
        for item in self.data.values():
            x_coord = random.randint(0, 30)
            y_coord = random.randint(0, 30)
            while (x_coord, y_coord) in used_coordinates:
                x_coord = random.randint(0, 30)
                y_coord = random.randint(0, 30)
            used_coordinates.add((x_coord, y_coord))
            item['x_coord'].setText(str(x_coord))
            item['y_coord'].setText(str(y_coord))

        # Clear existing connections before generating new ones
        for item in self.data.values():
            item['connections'].clear()  
            
        for label_char, item in self.data.items():
            existing_labels = list(self.data.keys())  # Get list of existing labels
            existing_labels.remove(label_char)  # Remove own label from list
            num_connections = random.randint(1, len(existing_labels))  # Determine number of connections (at least 1)
            random_connections = random.sample(existing_labels, num_connections)  # Sample random connections

            # Ensure bidirectional connections and handle the case where label_char is in random_connections
            for connected_label in random_connections:
                # Append connected_label to the connections of label_char
                existing_connections_label_char = item['connections'].text().split(', ')
                if connected_label not in existing_connections_label_char:
                    existing_connections_label_char.append(connected_label)
                updated_connections_label_char = ", ".join(existing_connections_label_char).lstrip(', ')  # Strip leading comma
                item['connections'].setText(updated_connections_label_char)

                # Append label_char to the connections of connected_label
                existing_connections_connected_label = self.data[connected_label]['connections'].text().split(', ')
                if label_char not in existing_connections_connected_label:
                    existing_connections_connected_label.append(label_char)
                updated_connections_connected_label = ", ".join(existing_connections_connected_label).lstrip(', ')  # Strip leading comma
                self.data[connected_label]['connections'].setText(updated_connections_connected_label)



          


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()