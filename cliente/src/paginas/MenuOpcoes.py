import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from ControladoraCliente import *
from Categoria import Categoria

class MenuOpcoes(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.criaMenu()
    
    def criaMenu(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # opcoes do menu
        categoria_botoes = []
        for categoria in Categoria:
            categoria_botoes.append(QPushButton(categoria.value))

        for botao in categoria_botoes:
            main_layout.addWidget(botao)

        self.setLayout(main_layout)