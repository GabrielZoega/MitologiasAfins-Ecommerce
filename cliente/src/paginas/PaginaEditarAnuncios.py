import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt
from paginas.GridAnunciosVendedor import *
from paginas.MenuOpcoes import *
from ControladoraCliente import ControladoraCliente
from Produto import Produto
from TipoCliente import TipoCliente

class PaginaEditarAnuncios(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        # self.cliente.produtos_user_recuperados.connect(self.criaPagina)
        self.criaPagina()
        

    def criaPagina(self):
        # Layout principal horizontal
        main_layout = QHBoxLayout()

        # Adiciona um espaço na esquerda para centralizar horizontalmente
        # main_layout.addStretch(1)

        # anuncios
        anuncios_layout = QVBoxLayout()

        titulo_label = QLabel("Anúncios da sua loja:")
        anuncios_layout.addWidget(titulo_label)


        # anuncios
        # for produto in produtos:
        #     anuncio_layout = QHBoxLayout()
        #     anuncio_nome_label = QLabel(produto.nome)
        #     anuncio_editar_botao = QPushButton("Editar")

        #     anuncio_layout.addWidget(anuncio_nome_label)
        #     anuncio_layout.addWidget(anuncio_editar_botao)
        #     anuncios_layout.addLayout(anuncio_layout)

        anuncios_grid = GridAnunciosVendedor(paginas=self.paginas, tipo_usuario=TipoCliente.VENDEDOR, cliente=self.cliente)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(anuncios_grid)

        anuncios_layout.addWidget(scroll_area)

        # opcoes de anuncio
        opcoes_layout = QVBoxLayout()
        criar_anuncio_botao = QPushButton("Criar Anúncio")
        criar_anuncio_botao.clicked.connect(self.irParaCriarAnuncio)
        opcoes_layout.addWidget(criar_anuncio_botao)

        # adiciona os widgets ao layout da pagina
        main_layout.addLayout(anuncios_layout)
        main_layout.addLayout(opcoes_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        # main_layout.addStretch()

        # define o layout principal para o widget
        self.setLayout(main_layout)

    def irParaCriarAnuncio(self):
        self.paginas.setCurrentIndex(self.paginas.PAGINA_CRIAR_ANUNCIO)