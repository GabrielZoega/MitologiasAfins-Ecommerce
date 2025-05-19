import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from paginas.GridAnuncios import *
from paginas.MenuOpcoes import *
from ControladoraCliente import *
from TipoCliente import TipoCliente

class PaginaPesquisa(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.criaPagina()
        

    def criaPagina(self):
        # layout principal horizontal
        main_layout = QHBoxLayout()

        # adiciona um espaço na esquerda para centralizar horizontalmente
        # main_layout.addStretch(1)

        # layout para o centro da página
        centro_layout = QVBoxLayout()

        # layout para a barra de pesquisa
        barra_pesquisa_layout = QHBoxLayout()

        # menu
        menu = MenuOpcoes(paginas=self.paginas, cliente=self.cliente)

        # barra de pesquisa
        self.pesquisa_input = QLineEdit()
        self.pesquisa_input.setPlaceholderText("Pesquise aqui...")
        self.pesquisa_input.setFixedWidth(300) 
        pesquisa_botao = QPushButton("Pesquisar")
        # pesquisa_botao.clicked.connect()
        barra_pesquisa_layout.addWidget(self.pesquisa_input)
        barra_pesquisa_layout.addWidget(pesquisa_botao)
        barra_pesquisa_layout.addStretch()      

        # label com resultado de pesquisa
        resultado_label = QLabel("Resultados para \"...\":")

        # anuncios
        anuncios_grid = GridAnuncios(paginas=self.paginas, cliente=self.cliente, tipo_usuario=TipoCliente.COMPRADOR)

        # centro da pagina
        centro_layout.addLayout(barra_pesquisa_layout)
        centro_layout.addWidget(anuncios_grid)
        
        # adiciona os widgets ao layout da pagina
        main_layout.addWidget(menu)
        main_layout.addLayout(centro_layout)

        # adiciona um espaço na direita para centralizar o formulario horizontalmente
        # main_layout.addStretch()

        # define o layout principal para o widget
        self.setLayout(main_layout)


