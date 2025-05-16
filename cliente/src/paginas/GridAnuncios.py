import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from ControladoraCliente import *

class GridAnuncios(QWidget):
    def __init__(self, paginas: QStackedWidget, tipo_usuario, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.tipo_usuario = tipo_usuario
        self.criaGrid()
        self.carrega_anuncios()

    def criaGrid(self):

        main_layout = QGridLayout()

        self.setLayout(main_layout)

    def carrega_anuncios(self):
        self.cliente.recuperaAnuncios()
        # print(anuncios)
    

class WidgetAnuncio(QWidget):
    def __init__(self, paginas: QStackedWidget, caminho_imagem):
        super().__init__()
        self.paginas = paginas
        self.criaWidget(caminho_imagem)
        

    def criaWidget(self, caminho_imagem):
        
        anuncio = QPushButton()
        anuncio.setIcon(QIcon())
        anuncio.setIconSize(QSize(32, 32))
        anuncio.clicked.connect()
    

