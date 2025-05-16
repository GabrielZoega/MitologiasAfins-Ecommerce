
import sys
from PyQt6.QtWidgets import QApplication
from interface import MainWindow
from ControladoraCliente import ControladoraCliente
import threading


app = QApplication(sys.argv)
controladora_cliente = ControladoraCliente()
controladora_cliente.estabeleceConexao()

window = MainWindow(cliente=controladora_cliente)
window.show()

app.exec()