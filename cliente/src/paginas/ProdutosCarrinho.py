import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import QSize, Qt  
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon 
from ControladoraCliente import ControladoraCliente

class ProdutosCarrinho(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente, produtosCarrinho):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.produtosCarrinho = produtosCarrinho
        self.criaCarrinho()
    
    def criaCarrinho(self):

        main_layout = QVBoxLayout()

        for produto in self.produtosCarrinho:
            main_layout.addWidget(ProdutoCarrinho(paginas=self.paginas, cliente=self.cliente, produto=produto))

        self.setLayout(main_layout)


class ProdutoCarrinho(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente, produto):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.produto = produto
        self.criaProduto()

    
    def criaProduto(self):

        main_layout = QHBoxLayout()

        # imagem do produto
        # imagem = QIcon()

        # nome do produto
        nome = QLabel(self.cliente.getNomeProduto(self.produto.idProduto))

        # botao de diminuir a quantidade
        diminuir_botao = QPushButton("-")
        diminuir_botao.setMaximumSize(QSize(32, 32))
        diminuir_botao.clicked.connect(self.diminuiQuantidade)

        # quantidade
        quantidade = QLabel(str(self.produto.quantidadeCarrinho))
        quantidade.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quantidade.setMaximumSize(QSize(50, 32))

        # botao de aumentar a quantidade
        aumentar_botao = QPushButton("+")
        aumentar_botao.setMaximumSize(QSize(32, 32))
        aumentar_botao.clicked.connect(self.aumentaQuantidade)

        # botao de excluir do carrinho
        excluir_botao = QPushButton()
        excluir_botao.setIcon(QAbstractFileIconProvider().icon(QAbstractFileIconProvider.IconType.Trashcan))
        excluir_botao.setIconSize(QSize(27, 27))
        excluir_botao.setMaximumSize(QSize(32, 32))
        excluir_botao.setStyleSheet("background-color: red;")
        excluir_botao.clicked.connect(self.excluiProduto)


        # main_layout.addWidget(imagem)
        main_layout.addWidget(nome)
        main_layout.addWidget(diminuir_botao)
        main_layout.addWidget(quantidade)
        main_layout.addWidget(aumentar_botao)
        main_layout.addWidget(excluir_botao)

        self.setLayout(main_layout)
    
    def diminuiQuantidade(self):
        if self.produto.quantidadeCarrinho > 0:
            self.cliente.alterarQuantidade(self.produto.idItem, self.produto.quantidadeCarrinho - 1)
            self.cliente.itens_carrinho_alterados.emit(True)

    def aumentaQuantidade(self):
        self.cliente.alterarQuantidade(self.produto.idItem, self.produto.quantidadeCarrinho + 1)
        self.cliente.itens_carrinho_alterados.emit(True)

    def excluiProduto(self):
        self.cliente.alterarQuantidade(self.produto.idItem, 0)
        self.cliente.itens_carrinho_alterados.emit(True)
        return