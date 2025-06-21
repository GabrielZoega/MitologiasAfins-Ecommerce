
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
from paginas.PaginaCriarAnuncio import *

from ControladoraCliente import ControladoraCliente
from TipoCliente import TipoCliente

class MainWindow(QMainWindow):
    
    def __init__(self, cliente: ControladoraCliente):
        super().__init__()


        self.cliente = cliente
        self.cliente.login_validado.connect(self.atualizaTipoUsuario)
        self.cliente.loja_recuperada.connect(self.atualizaTipoUsuario)
        self.cliente.loja_criada.connect(self.atualizaTipoUsuario)
        self.cliente.loja_excluida.connect(self.atualizaTipoUsuario)
        self.cliente.itens_carrinho_alterados.connect(self.paginaCarrinho)


        self.setWindowTitle("Mitologias&Afins")
        self.resize(QSize(960, 540))
        
        self.setStyleSheet("background-color: #323031; color: #E2E2E2")

        # adiciona a barra de ferramentas
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.addToolBar(self.toolbar)

        # botao para mudar o tema
        self.tema = {"modo": "Tema escuro"}
        self.action_mudar_tema = QAction(self.tema["modo"], self)
        self.action_mudar_tema.triggered.connect(lambda: self.mudaTema(tema=self.tema))
        self.toolbar.addAction(self.action_mudar_tema)

        # pilha de telas
        self.paginas = Paginas()

        # botao para ir para a pagina inicial
        self.action_ir_pagina_inicial = QAction("Página Inicial")
        self.action_ir_pagina_inicial.triggered.connect(self.paginaInicial)
        self.toolbar.addAction(self.action_ir_pagina_inicial)

        # botao para ir para a pagina de login
        self.action_ir_pagina_login = QAction("Login")
        self.action_ir_pagina_login.triggered.connect(self.paginaLogin)
        self.toolbar.addAction(self.action_ir_pagina_login)

        # botao para ir para a pagina de carrinho
        self.action_ir_pagina_carrinho = QAction("Carrinho")
        self.action_ir_pagina_carrinho.triggered.connect(self.paginaCarrinho)
        self.toolbar.addAction(self.action_ir_pagina_carrinho)

        # botao para ir para a pagina de criar ou editar loja

        self.action_ir_pagina_editar_loja = QAction("Editar loja")
        self.action_ir_pagina_criar_loja = QAction("Criar loja")

        self.action_ir_pagina_editar_loja.triggered.connect(self.paginaEditarLoja)
        self.action_ir_pagina_criar_loja.triggered.connect(self.paginaCriarLoja)

        self.toolbar.addAction(self.action_ir_pagina_criar_loja)
        

        # adiciona as paginas na pilha de widgets
        self.pagina_login = PaginaLogin(paginas=self.paginas, cliente=self.cliente)
        self.pagina_inicial = PaginaInicial(paginas=self.paginas, cliente=self.cliente)
        self.pagina_cadastro = PaginaCadastro(paginas=self.paginas, cliente=self.cliente)
        self.pagina_carrinho = PaginaCarrinho(paginas=self.paginas, cliente=self.cliente)
        self.pagina_pesquisa = PaginaPesquisa(paginas=self.paginas, cliente=self.cliente)
        self.pagina_criar_loja = PaginaCriarLoja(paginas=self.paginas, cliente=self.cliente)
        self.pagina_editar_loja = PaginaEditarLoja(paginas=self.paginas, cliente=self.cliente)
        self.pagina_editar_anuncio = PaginaEditarAnuncio(paginas=self.paginas, cliente=self.cliente, anuncio=None, produto=None)
        self.pagina_editar_anuncios = PaginaEditarAnuncios(paginas=self.paginas, cliente=self.cliente)
        self.pagina_criar_anuncio = PaginaCriarAnuncio(paginas=self.paginas, cliente=self.cliente)

        self.paginas.addWidget(self.pagina_login)           # 0
        self.paginas.addWidget(self.pagina_cadastro)        # 1
        self.paginas.addWidget(self.pagina_inicial)         # 2
        self.paginas.addWidget(self.pagina_carrinho)        # 3
        self.paginas.addWidget(self.pagina_criar_loja)      # 4
        self.paginas.addWidget(self.pagina_editar_loja)     # 5
        self.paginas.addWidget(self.pagina_editar_anuncio)  # 6
        self.paginas.addWidget(self.pagina_editar_anuncios) # 7
        self.paginas.addWidget(self.pagina_pesquisa)        # 8
        self.paginas.addWidget(self.pagina_criar_anuncio)   # 9

        self.setCentralWidget(self.paginas)  
        self.paginas.setCurrentIndex(self.paginas.PAGINA_INICIAL)     


    def mudaTema(self, tema):
        if(tema["modo"] == "Tema escuro"):
            self.setStyleSheet("background-color: #BBBAC6; color: #323031")
            tema["modo"] = "Tema claro"            
        else:
            self.setStyleSheet("background-color: #323031; color: #E2E2E2")
            tema["modo"] = "Tema escuro"

        self.action_mudar_tema.setText(tema["modo"])

    def paginaLogin(self):
        self.paginas.setCurrentIndex(self.paginas.PAGINA_LOGIN)

    def paginaInicial(self):
        self.cliente.recuperaAnuncios()
        self.paginas.setCurrentIndex(self.paginas.PAGINA_INICIAL)

    def paginaCarrinho(self):
        self.pagina_carrinho.criaPagina()
        self.paginas.setCurrentIndex(self.paginas.PAGINA_CARRINHO)

    def paginaCriarLoja(self):
        self.paginas.setCurrentIndex(self.paginas.PAGINA_CRIAR_LOJA)

    def paginaEditarLoja(self):
        self.paginas.setCurrentIndex(self.paginas.PAGINA_EDITAR_LOJA)

    def atualizaTipoUsuario(self, sucesso:bool):
        if sucesso:
            print("Atualizando tipo de usuário...")
            if self.cliente.usuario.tipoCliente == TipoCliente.VENDEDOR:
                self.toolbar.removeAction(self.action_ir_pagina_criar_loja)
                self.toolbar.addAction(self.action_ir_pagina_editar_loja)
            else:
                self.toolbar.removeAction(self.action_ir_pagina_editar_loja)
                self.toolbar.addAction(self.action_ir_pagina_criar_loja)
            


class Paginas(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.PAGINA_LOGIN = 0
        self.PAGINA_CADASTRO = 1
        self.PAGINA_INICIAL = 2
        self.PAGINA_CARRINHO = 3
        self.PAGINA_CRIAR_LOJA = 4
        self.PAGINA_EDITAR_LOJA = 5
        self.PAGINA_EDITAR_ANUNCIO = 6
        self.PAGINA_EDITAR_ANUNCIOS = 7
        self.PAGINA_PESQUISA = 8
        self.PAGINA_CRIAR_ANUNCIO = 9
        self.PAGINA_ANUNCIO = 10
