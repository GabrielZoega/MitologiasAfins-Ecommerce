import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from ControladoraCliente import ControladoraCliente
from Categoria import Categoria
from paginas.PaginaAnuncio import PaginaAnuncio
from Status import Status
from Produto import Produto
from Anuncio import Anuncio
from TipoCliente import TipoCliente

class GridAnuncios(QWidget):
    def __init__(self, paginas: QStackedWidget, tipo_usuario: TipoCliente, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.tipo_usuario = tipo_usuario
        self.widgets_anuncios = []
        self.cliente.anuncios_recuperados.connect(self.atualizaAnuncios)
        self.cliente.produtos_recuperados.connect(self.atualizaProdutos) 
        self.cliente.anuncio_criado.connect(self.atualizaAnuncios)
        self.cliente.anuncios_user_recuperados.connect(self.atualizaAnuncios)
        self.pesquisa = None
        self.criaGrid()
        self.carrega_anuncios() 

    def criaGrid(self):

        self.main_layout = QGridLayout()

        self.setLayout(self.main_layout)

    def carrega_anuncios(self):
        self.cliente.recuperaAnuncios()

    def atualizaAnuncios(self):
        if self.tipo_usuario == TipoCliente.COMPRADOR:
            # print("\nAtualizando anuncios comprador\n")
            self.cliente.recuperaProdutos()

    def atualizaProdutos(self):
        # print("Atualizando produtos")
        self.widgets_anuncios.clear()

        # retira todos os widgets do layout
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        # adiciona os anuncios ao layout
        # print(f"\n\n1 {self.tipo_usuario == TipoCliente.COMPRADOR}")
        
        anuncios = self.cliente.anuncios
        produtos = self.cliente.produtos
        for anuncio in anuncios:
            produto = None
            # print(f"3 {anuncio.status == Status.ATIVO}")
            if anuncio.status == Status.ATIVO:
                for p in produtos:
                    if p.idProduto == anuncio.idProduto:
                        produto = p
                        break

            if produto is not None:
                widget_anuncio = WidgetAnuncio(paginas=self.paginas, cliente=self.cliente, produto=produto, anuncio=anuncio, tipo_usuario=self.tipo_usuario)
                self.widgets_anuncios.append(widget_anuncio)
                self.main_layout.addWidget(widget_anuncio)
        
    def realizaPesquisa(self, pesquisaTipo: str, pesquisa: str):
        self.widgets_anuncios.clear()

        # retira todos os widgets do layout
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        # adiciona os anuncios ao layout
        # print(f"\n\n1 {self.tipo_usuario == TipoCliente.COMPRADOR}")
        
        anuncios = self.cliente.anuncios
        produtos = self.cliente.produtos

        produtos_pesquisados = []
        anuncios_pesquisados = []
        if pesquisaTipo == "normal":
            anuncios_pesquisados = anuncios
            for produto in produtos:
                if pesquisa.lower() in produto.nome.lower():
                    produtos_pesquisados.append(produto)
        
        elif pesquisaTipo == "categoria":
            produtos_pesquisados = produtos
            for anuncio in anuncios:
                print(f"\n\n Anuncio.categoria: {Categoria[anuncio.categoria].value}\nPesquisa: {pesquisa}\n\n")
                if pesquisa == Categoria[anuncio.categoria].value:
                    anuncios_pesquisados.append(anuncio)
        
        
        for anuncio in anuncios_pesquisados:
            produto = None
            # print(f"3 {anuncio.status == Status.ATIVO}")
            if anuncio.status == Status.ATIVO:
                for p in produtos_pesquisados:
                    if p.idProduto == anuncio.idProduto:
                        produto = p
                        break

            if produto is not None:
                widget_anuncio = WidgetAnuncio(paginas=self.paginas, cliente=self.cliente, produto=produto, anuncio=anuncio, tipo_usuario=self.tipo_usuario)
                self.widgets_anuncios.append(widget_anuncio)
                self.main_layout.addWidget(widget_anuncio)

class WidgetAnuncio(QWidget):

    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente, produto: Produto, anuncio: Anuncio, tipo_usuario: TipoCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.produto = produto
        self.anuncio = anuncio
        self.tipo_usuario = tipo_usuario
        self.criaWidget()
        self.setStyleSheet("background: rgba(0, 0, 0, 0.1);")
        self.setMouseTracking(True)

    def criaWidget(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)           
        self.layout.setContentsMargins(0, 0, 0, 0) 
        self.setLayout(self.layout)

        # Você pode remover o QPushButton se quiser o widget inteiro clicável
        # anuncio_imagem = QPushButton()
        # anuncio_imagem.setIcon(QIcon())
        # anuncio_imagem.setIconSize(QSize(32, 32))
        # anuncio_imagem.clicked.connect(self.abreAnuncio)
        # self.layout.addWidget(anuncio_imagem)

        # nome do produto
        nome_label = QLabel(self.produto.nome)
        self.layout.addWidget(nome_label)
        # preco do produto
        preco_label = QLabel(f"R$ {self.produto.preco:.2f}")
        self.layout.addWidget(preco_label)
        self.setFixedSize(200, 200)

    def mousePressEvent(self, event):
        self.abreAnuncio()

    def enterEvent(self, event):
        self.setStyleSheet("background: rgba(0, 0, 0, 0.2);")

    def leaveEvent(self, event):
        self.setStyleSheet("background: rgba(0, 0, 0, 0.1);")

    def abreAnuncio(self):

        self.pagina_anuncio = PaginaAnuncio(paginas=self.paginas, cliente=self.cliente, pagina_anterior=self.paginas.currentIndex(), produto=self.produto, anuncio=self.anuncio)
        self.paginas.addWidget(self.pagina_anuncio) 
        self.paginas.setCurrentIndex(self.paginas.PAGINA_ANUNCIO)

    