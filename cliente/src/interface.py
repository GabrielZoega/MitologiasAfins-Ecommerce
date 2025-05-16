
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QToolBar, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
from PyQt6.QtGui import QColor, QPalette, QAction

from paginas.PaginaLogin import *
from paginas.PaginaCadastro import *
from paginas.PaginaInicial import *
from paginas.PaginaCarrinho import *
from paginas.PaginaCriarLoja import *
from paginas.PaginaEditarLoja import *
from paginas.PaginaAnuncio import *
from paginas.PaginaEditarAnuncios import *
from paginas.PaginaEditarAnuncio import *
from paginas.PaginaPesquisa import *

from ControladoraCliente import ControladoraCliente

PAGINA_LOGIN = 0
PAGINA_CADASTRO = 1
PAGINA_INICIAL = 2
PAGINA_CARRINHO = 3
PAGINA_CRIAR_LOJA = 4
PAGINA_EDITAR_LOJA = 5
PAGINA_ANUNCIO = 6
PAGINA_EDITAR_ANUNCIO = 7
PAGINA_EDITAR_ANUNCIOS = 8
PAGINA_PESQUISA = 9

class MainWindow(QMainWindow):
    
    def __init__(self, cliente: ControladoraCliente):
        super().__init__()

        self.cliente = cliente


        self.setWindowTitle("Mitologias&Afins")
        self.resize(QSize(960, 540))
        
        self.setStyleSheet("background-color: #323031; color: #E2E2E2")

        # adiciona a barra de ferramentas
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.addToolBar(toolbar)

        # botao para mudar o tema
        self.tema = {"modo": "Tema escuro"}
        self.action_mudar_tema = QAction(self.tema["modo"], self)
        self.action_mudar_tema.triggered.connect(lambda: self.mudaTema(tema=self.tema))
        toolbar.addAction(self.action_mudar_tema)
        
        # pilha de telas
        self.paginas = QStackedWidget()

        # botao para ir para a pagina inicial
        self.action_ir_pagina_inicial = QAction("Página Inicial")
        self.action_ir_pagina_inicial.triggered.connect(self.paginaInicial)
        toolbar.addAction(self.action_ir_pagina_inicial)

        # botao para ir para a pagina de login
        self.action_ir_pagina_login = QAction("Login")
        self.action_ir_pagina_login.triggered.connect(self.paginaLogin)
        toolbar.addAction(self.action_ir_pagina_login)

        # botao para ir para a pagina de carrinho
        self.action_ir_pagina_carrinho = QAction("Carrinho")
        self.action_ir_pagina_carrinho.triggered.connect(self.paginaCarrinho)
        toolbar.addAction(self.action_ir_pagina_carrinho)

        # botao para ir para a pagina de criar ou editar loja
        self.action_ir_pagina_criar_loja = QAction("Criar loja")
        self.action_ir_pagina_criar_loja.triggered.connect(self.paginaCriarLoja)
        toolbar.addAction(self.action_ir_pagina_criar_loja)
        
        self.action_ir_pagina_editar_loja = QAction("Editar loja")
        self.action_ir_pagina_editar_loja.triggered.connect(self.paginaEditarLoja)
        toolbar.addAction(self.action_ir_pagina_editar_loja)

        # adiciona as paginas na pilha de widgets
        self.pagina_login = PaginaLogin(paginas=self.paginas, cliente=self.cliente)
        self.pagina_inicial = PaginaInicial(paginas=self.paginas, cliente=self.cliente)
        # self.pagina_anuncio = PaginaAnuncio(paginas=self.paginas, cliente=self.cliente)
        self.pagina_cadastro = PaginaCadastro(paginas=self.paginas, cliente=self.cliente)
        self.pagina_carrinho = PaginaCarrinho(paginas=self.paginas, cliente=self.cliente)
        self.pagina_pesquisa = PaginaPesquisa(paginas=self.paginas, cliente=self.cliente)
        self.pagina_criar_loja = PaginaCriarLoja(paginas=self.paginas, cliente=self.cliente)
        self.pagina_editar_loja = PaginaEditarLoja(paginas=self.paginas, cliente=self.cliente)
        # self.pagina_editar_anuncio = PaginaEditarAnuncio(paginas=self.paginas, cliente=self.cliente)
        self.pagina_editar_anuncios = PaginaEditarAnuncios(paginas=self.paginas, cliente=self.cliente)

        self.paginas.addWidget(self.pagina_login)           # 0
        self.paginas.addWidget(self.pagina_cadastro)        # 1
        self.paginas.addWidget(self.pagina_inicial)         # 2
        self.paginas.addWidget(self.pagina_carrinho)        # 3
        self.paginas.addWidget(self.pagina_criar_loja)      # 4
        self.paginas.addWidget(self.pagina_editar_loja)     # 5
        # self.paginas.addWidget(self.pagina_anuncio)         # 6
        # self.paginas.addWidget(self.pagina_editar_anuncio)  # 7
        self.paginas.addWidget(self.pagina_editar_anuncios) # 8
        self.paginas.addWidget(self.pagina_pesquisa)        # 9

        self.setCentralWidget(self.paginas)  
        self.paginas.setCurrentIndex(2)     
        
   

    def mudaTema(self, tema):
        if(tema["modo"] == "Tema escuro"):
            self.setStyleSheet("background-color: #BBBAC6; color: #323031")
            tema["modo"] = "Tema claro"            
        else:
            self.setStyleSheet("background-color: #323031; color: #E2E2E2")
            tema["modo"] = "Tema escuro"

        self.action_mudar_tema.setText(tema["modo"])

    def paginaLogin(self):
        self.paginas.setCurrentIndex(PAGINA_LOGIN)

    def paginaInicial(self):
        self.paginas.setCurrentIndex(PAGINA_INICIAL)

    def paginaCarrinho(self):
        self.paginas.setCurrentIndex(PAGINA_CARRINHO)

    def paginaCriarLoja(self):
        self.paginas.setCurrentIndex(PAGINA_CRIAR_LOJA)

    def paginaEditarLoja(self):
        self.paginas.setCurrentIndex(PAGINA_EDITAR_LOJA)

        


