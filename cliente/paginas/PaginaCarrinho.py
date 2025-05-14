from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from paginas.GridAnuncios import *
from paginas.MenuOpcoes import *
from paginas.ProdutosCarrinho import *

class PaginaCarrinho(QWidget):
    def __init__(self, paginas: QStackedWidget):
        super().__init__()
        self.paginas = paginas
        self.criaPagina()
        

    def criaPagina(self):
        # layout principal horizontal
        main_layout = QHBoxLayout()

        # adiciona um espaço na esquerda para centralizar horizontalmente
        # main_layout.addStretch(1)

        # layout para o centro da página
        centro_layout = QVBoxLayout()

        # menu
        menu = MenuOpcoes(paginas=self.paginas)

        # label escrito Carrinho
        carrinho_label = QLabel("Carrinho")

        # produtos no carrinho
        lista_produtos = ProdutosCarrinho(paginas=self.paginas)

        # botao de fechar compra
        fechar_compra_botao = QPushButton("Fechar Compra")
        # fechar_compra_botao.clicked.connect()

        # centro da pagina
        centro_layout.addWidget(carrinho_label)
        centro_layout.addWidget(lista_produtos)
        centro_layout.addWidget(fechar_compra_botao)
        
        # adiciona os widgets ao layout da pagina
        main_layout.addWidget(menu)
        main_layout.addLayout(centro_layout)

        # adiciona um espaço na direita para centralizar o formulario horizontalmente
        # main_layout.addStretch()

        # define o layout principal para o widget
        self.setLayout(main_layout)


