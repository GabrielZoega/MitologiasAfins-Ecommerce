from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from paginas.GridAnuncios import *
from paginas.MenuOpcoes import *

class PaginaInicial(QWidget):
    def __init__(self, paginas: QStackedWidget):
        super().__init__()
        self.paginas = paginas
        self.criaPagina()
        

    def criaPagina(self):
        # Layout principal horizontal
        main_layout = QHBoxLayout()

        # Adiciona um espaço na esquerda para centralizar horizontalmente
        # main_layout.addStretch(1)

        # layout para o centro da página
        centro_layout = QVBoxLayout()

        # layout para a barra de pesquisa
        barra_pesquisa_layout = QHBoxLayout()

        # menu
        menu = MenuOpcoes(paginas=self.paginas)

        # barra de pesquisa
        self.pesquisa_input = QLineEdit()
        self.pesquisa_input.setPlaceholderText("Pesquise aqui...")
        pesquisa_botao = QPushButton("Pesquisar")
        # pesquisa_botao.clicked.connect()
        barra_pesquisa_layout.addWidget(self.pesquisa_input)
        barra_pesquisa_layout.addWidget(pesquisa_botao)

        # anuncios
        anuncios_grid = GridAnuncios(paginas=self.paginas, tipo_usuario="Cliente")

        # centro da pagina
        centro_layout.addLayout(barra_pesquisa_layout)
        centro_layout.addWidget(anuncios_grid)
        
        # adiciona os widgets ao layout da pagina
        main_layout.addWidget(menu)
        main_layout.addLayout(centro_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        # main_layout.addStretch()

        # define o layout principal para o widget
        self.setLayout(main_layout)
