import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from PyQt5.QtCore import Qt

class PopupResultados(QDialog):
    def __init__(self, heuristica, datos):
        super().__init__()

        if heuristica == 0:
            self.setWindowTitle("Resultados de búsqueda: heurística euclídea")
        else:
            self.setWindowTitle("Resultados de búsqueda: heurística Manhattan")
        self.resize(400, 170)

        self.datos = datos

        self.tabla = QTableWidget()
        self.tabla.setRowCount(4)
        self.tabla.setColumnCount(2)

        self.tabla.setHorizontalHeaderLabels(["Escalada simple", "Máxima pendiente"])

        self.tabla.setVerticalHeaderLabels(["Llegó al final", "Camino recorrido", "Cant. saltos", "Cant. pasos"])

        self.cargar_datos()

        self.bloquear_celdas()

        layout = QVBoxLayout()
        layout.addWidget(self.tabla)

        # Ajustar el tamaño de la tabla al de la ventana
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setLayout(layout)

    def cargar_datos(self):
        for i in range(4):
            for j in range(2):
                item = QTableWidgetItem(self.datos[i][j])
                self.tabla.setItem(i, j, item)
                print(i, j, self.datos[i][j])

    def bloquear_celdas(self):
        for i in range(self.tabla.rowCount()):
            for j in range(self.tabla.columnCount()):
                item = self.tabla.item(i, j)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PopupResultados()
    window.show()
    sys.exit(app.exec_())
