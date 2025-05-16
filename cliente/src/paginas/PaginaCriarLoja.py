import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from ControladoraCliente import *

class PaginaCriarLoja(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.criaPagina()
        

    def criaPagina(self):
        # layout principal horizontal
        main_layout = QHBoxLayout()

        # adiciona um espaco na esquerda para centralizar horizontalmente
        main_layout.addStretch(1)

        # layout para o formulario 
        form_layout = QVBoxLayout() 

        # titulo do formulario
        titulo_label = QLabel("Cadastre sua loja:")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # nome
        nome_layout = QHBoxLayout()
        nome_label = QLabel("Nome:")
        self.nome_input = QLineEdit()
        nome_layout.addWidget(nome_label)
        nome_layout.addWidget(self.nome_input)

        # descricao
        descricao_layout = QHBoxLayout()
        descricao_label = QLabel("Descrição:")
        self.descricao_input = QLineEdit()
        descricao_layout.addWidget(descricao_label)
        descricao_layout.addWidget(self.descricao_input)

        # endereco
        endereco_layout = QHBoxLayout()
        endereco_label = QLabel("Endereço:")
        self.endereco_input = QLineEdit()
        endereco_layout.addWidget(endereco_label)
        endereco_layout.addWidget(self.endereco_input)

        # botao de criar loja
        criar_loja_botao = QPushButton("Criar Loja")
        # criar_loja_botao.clicked.connect()

        # status da criacao da loja
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adiciona os widgets de entrada ao layout do formulario
        form_layout.addWidget(titulo_label)
        form_layout.addLayout(nome_layout)
        form_layout.addLayout(descricao_layout)
        form_layout.addLayout(endereco_layout)
        form_layout.addWidget(criar_loja_botao)
        form_layout.addWidget(self.status_label)

        # Adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)

