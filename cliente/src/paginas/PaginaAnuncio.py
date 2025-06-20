import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ControladoraCliente import ControladoraCliente
from Produto import Produto
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget
from PyQt6.QtCore import Qt
from Produto import Produto
from Anuncio import Anuncio

class PaginaAnuncio(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente, pagina_anterior: int, produto: Produto, anuncio: Anuncio):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.pagina_anterior = pagina_anterior
        self.produto = produto
        self.anuncio = anuncio
        self.criaPagina()
    
    def criaPagina(self):
        # layout principal horizontal
        main_layout = QHBoxLayout()

        # layout para a barra lateral
        barra_lateral = QVBoxLayout()

        # layout para o produto 
        produto_layout = QVBoxLayout()
        produto_layout.setSpacing(0)
        produto_layout.setContentsMargins(0, 0, 0, 0)
        produto_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        produto_widget = QWidget()
        produto_widget.setLayout(produto_layout)
        produto_widget.setMaximumWidth(400)  
        produto_widget.setMaximumHeight(600)

        # botao de voltar
        voltar_botao = QPushButton("Voltar")
        voltar_botao.setFixedSize(100, 30)
        voltar_botao.clicked.connect(self.voltarParaPaginaAnterior)
        barra_lateral.addWidget(voltar_botao)
        barra_lateral.addStretch()

        # produto
        nome_label = QLabel(self.produto.nome)
        nome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        produto_layout.addWidget(nome_label)
        # imagem
        preco_label = QLabel(f"R$ {self.produto.preco:.2f}")
        preco_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        produto_layout.addWidget(preco_label)

        estoque_label = QLabel(f"Estoque: {self.produto.estoque}")
        estoque_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        produto_layout.addWidget(estoque_label)

        # botao de adicionar ao carrinho
        adicionar_botao = QPushButton("Adicionar ao Carrinho")
        adicionar_botao.setFixedSize(200, 25)
        adicionar_botao.clicked.connect(self.adicionarAoCarrinho)
        produto_layout.addWidget(adicionar_botao)

        # descricao
        descricao_layout = QHBoxLayout()
        descricao_titulo_label = QLabel("Descrição: ")
        descricao_label = QLabel(self.produto.descricao)
        descricao_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descricao_layout.addWidget(descricao_titulo_label)
        descricao_layout.addWidget(descricao_label)
        produto_layout.addLayout(descricao_layout)

        # status de adicionar ao carrinho
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        produto_layout.addWidget(self.status_label)

        # adiciona os layouts ao layout principal
        main_layout.addLayout(barra_lateral)
        main_layout.addStretch()
        main_layout.addWidget(produto_widget) 
        main_layout.addStretch()

        # define o layout principal para o widget
        self.setLayout(main_layout)


    def voltarParaPaginaAnterior(self):
        self.paginas.setCurrentIndex(self.pagina_anterior)
        self.paginas.removeWidget(self)

    def adicionarAoCarrinho(self):
        if self.cliente.usuario.idUser is None:
            self.status_label.setText("Você precisa estar logado.")
            return
        else:
            self.status_label.setText("Produto adicionado ao carrinho com sucesso.")
            self.cliente.adicionarItem(self.cliente.usuario.idCarrinho, self.produto.idProduto, 1)
