import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from paginas.GridAnuncios import *
from paginas.MenuOpcoes import *
from paginas.ProdutosCarrinho import *
from ControladoraCliente import ControladoraCliente

class PaginaCarrinho(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.criaPagina()
        

    def criaPagina(self):
        layout_antigo = self.layout()
        if layout_antigo is not None:
            self.resetar_layout(layout_antigo)
            
            # layout principal horizontal
            main_layout = layout_antigo
        else:
            # layout principal horizontal
            main_layout = QHBoxLayout()
            self.setLayout(main_layout)

        # adiciona um espaço na esquerda para centralizar horizontalmente
        main_layout.addStretch(1)

        # layout para o centro da página
        centro_layout = QVBoxLayout()
        
        # adiciona espaço para centralizar o conteudo
        centro_layout.addStretch(1)

        # label escrito Carrinho
        carrinho_label = QLabel("Carrinho")
        carrinho_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        carrinho_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # produtos no carrinho
        self.lista_produtos = None
        if self.cliente.usuario.idUser is not None:
            self.lista_produtos = ProdutosCarrinho(paginas=self.paginas, cliente=self.cliente, produtosCarrinho=self.cliente.recuperaItens(self.cliente.usuario.idCarrinho))

        # botao de fechar compra
        fechar_compra_botao = QPushButton("Fechar Compra")
        fechar_compra_botao.clicked.connect(self.fecharCompra)

        # centro da pagina
        centro_layout.addWidget(carrinho_label)
        if self.lista_produtos is not None:
            centro_layout.addWidget(self.lista_produtos)
        centro_layout.addWidget(fechar_compra_botao)

        # mensagem de erro
        self.erro_label = QLabel("")
        self.erro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        centro_layout.addWidget(self.erro_label)

        # adiciona espaço para centralizar o conteudo
        centro_layout.addStretch(1)
        
        # adiciona os widgets ao layout da pagina
        main_layout.addLayout(centro_layout)

        # adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)


    def resetar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.resetar_layout(item.layout())

    def fecharCompra(self):
        resultado = self.cliente.fecharCarrinho(self.cliente.usuario.idCarrinho)
        if resultado == 403:
            print("Erro ao fechar o carrinho: ", resultado)
            self.erro_label.setText("Não há produtos suficientes no estoque.")
        else:
            if self.lista_produtos is not None:
                self.erro_label.setText("Compra realizada com sucesso!")
                print("Compra realizada com sucesso!")

            self.cliente.itens_carrinho_alterados.emit(True)