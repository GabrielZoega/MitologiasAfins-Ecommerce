from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from paginas.GridAnuncios import *
from paginas.MenuOpcoes import *

class PaginaEditarAnuncios(QWidget):
    def __init__(self, paginas: QStackedWidget):
        super().__init__()
        self.paginas = paginas
        self.criaPagina()
        

    def criaPagina(self):
        # Layout principal horizontal
        main_layout = QHBoxLayout()

        # Adiciona um espaço na esquerda para centralizar horizontalmente
        # main_layout.addStretch(1)

        # anuncios
        anuncios_grid = GridAnuncios(paginas=self.paginas, tipo_usuario="Vendedor")

        # adiciona os widgets ao layout da pagina
        main_layout.addWidget(anuncios_grid)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        # main_layout.addStretch()

        # define o layout principal para o widget
        self.setLayout(main_layout)
