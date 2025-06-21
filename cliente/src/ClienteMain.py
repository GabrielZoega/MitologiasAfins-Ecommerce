
import sys
from PyQt6.QtWidgets import QApplication
from interface import MainWindow
from ControladoraCliente import ControladoraCliente


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controladora_cliente = ControladoraCliente()

    window = MainWindow(cliente=controladora_cliente)
    window.show()

    app.exec()