import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from ControladoraCliente import ControladoraCliente
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
        # categoria_botoes = []
        # for categoria in Categoria:
        #     categoria_botoes.append(QPushButton(categoria.value))

        # for botao in categoria_botoes:
        #     print(f"Texto botao: {botao.text()}")
        #     botao.clicked.connect(lambda: self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", botao.text()))
        #     main_layout.addWidget(botao)


        botao_brasileiro = QPushButton(Categoria.FOLCLORE_BRASILEIRO.value)
        botao_brasileiro.clicked.connect(self.pesquisarBrasileiro)
        main_layout.addWidget(botao_brasileiro)

        botao_grego = QPushButton(Categoria.MITOLOGIA_GREGA.value)
        botao_grego.clicked.connect(self.pesquisarGrego)
        main_layout.addWidget(botao_grego)

        botao_romano = QPushButton(Categoria.MITOLOGIA_ROMANA.value)
        botao_romano.clicked.connect(self.pesquisarRomano)
        main_layout.addWidget(botao_romano)

        botao_nordica = QPushButton(Categoria.MITOLOGIA_NORDICA.value)
        botao_nordica.clicked.connect(self.pesquisarNordica)
        main_layout.addWidget(botao_nordica)

        botao_egipcia = QPushButton(Categoria.MITOLOGIA_EGIPCIA.value)
        botao_egipcia.clicked.connect(self.pesquisarEgipcia)
        main_layout.addWidget(botao_egipcia)

        botao_celta = QPushButton(Categoria.MITOLOGIA_CELTA.value)
        botao_celta.clicked.connect(self.pesquisarCelta)
        main_layout.addWidget(botao_celta)

        botao_outro = QPushButton(Categoria.OUTRO.value)
        botao_outro.clicked.connect(self.pesquisarOutro)
        main_layout.addWidget(botao_outro)


        self.setLayout(main_layout)

    def pesquisarBrasileiro(self):
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", Categoria.FOLCLORE_BRASILEIRO.value)
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{Categoria.FOLCLORE_BRASILEIRO.value}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)

    def pesquisarGrego(self):
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", Categoria.MITOLOGIA_GREGA.value)
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{Categoria.MITOLOGIA_GREGA.value}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)
    
    def pesquisarRomano(self):
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", Categoria.MITOLOGIA_ROMANA.value)
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{Categoria.MITOLOGIA_ROMANA.value}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)

    def pesquisarNordica(self):
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", Categoria.MITOLOGIA_NORDICA.value)
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{Categoria.MITOLOGIA_NORDICA.value}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)
    
    def pesquisarEgipcia(self):
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", Categoria.MITOLOGIA_EGIPCIA.value)
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{Categoria.MITOLOGIA_EGIPCIA.value}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)
    
    def pesquisarCelta(self):
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", Categoria.MITOLOGIA_CELTA.value)
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{Categoria.MITOLOGIA_CELTA.value}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)

    def pesquisarOutro(self):
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).anuncios_grid.realizaPesquisa("categoria", Categoria.OUTRO.value)
        self.paginas.widget(self.paginas.PAGINA_PESQUISA).resultado_label.setText(f"Resultados para \"{Categoria.OUTRO.value}\":")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_PESQUISA)

