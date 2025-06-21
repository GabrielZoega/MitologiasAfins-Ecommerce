import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt
from paginas.GridAnuncios import *
from paginas.MenuOpcoes import *
from ControladoraCliente import ControladoraCliente
from TipoCliente import TipoCliente

class PaginaInicial(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
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
        menu = MenuOpcoes(paginas=self.paginas, cliente=self.cliente)

        # barra de pesquisa
        self.pesquisa_input = QLineEdit()
        self.pesquisa_input.setFixedWidth(300) 
        self.pesquisa_input.setPlaceholderText("Pesquise aqui...")
        pesquisa_botao = QPushButton("Pesquisar")
        pesquisa_botao.clicked.connect(self.pesquisar)
        barra_pesquisa_layout.addStretch()
        barra_pesquisa_layout.addWidget(self.pesquisa_input)
        barra_pesquisa_layout.addWidget(pesquisa_botao)
        barra_pesquisa_layout.addStretch()

        # anuncios
        anuncios_grid = GridAnuncios(paginas=self.paginas, tipo_usuario=TipoCliente.COMPRADOR, cliente=self.cliente)

        # grid scrollavel
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(anuncios_grid)

        # centro da pagina
        centro_layout.addLayout(barra_pesquisa_layout)
        centro_layout.addWidget(scroll_area) 
        
        # adiciona os widgets ao layout da pagina
        main_layout.addWidget(menu)
        main_layout.addLayout(centro_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        # main_layout.addStretch()

        # define o layout principal para o widget
        self.setLayout(main_layout)

    def pesquisar(self):
        print("pesquisar")
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("normal", self.pesquisa_input.text())
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{self.pesquisa_input.text()}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)