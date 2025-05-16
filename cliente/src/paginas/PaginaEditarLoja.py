import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from ControladoraCliente import *

class PaginaEditarLoja(QWidget):
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

        # layout para as opcoes de anuncio
        opcoes_layout = QVBoxLayout()

        # layout para o formulario 
        form_layout = QVBoxLayout() 

        # opcoes de anuncio
        criar_anuncio_botao = QPushButton("Criar novo anúncio")
        # criar_anuncio_botao.clicked.connect()
        editar_anuncio_botao = QPushButton("Editar anúncio existente")
        # editar_anuncio_botao.clicked.connect()

        # titulo do formulario
        titulo_label = QLabel("Edite sua loja:")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # nome
        nome_layout = QHBoxLayout()
        nome_label = QLabel("Nome:")
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("")
        nome_layout.addWidget(nome_label)
        nome_layout.addWidget(self.nome_input)

        # descricao
        descricao_layout = QHBoxLayout()
        descricao_label = QLabel("Descrição:")
        self.descricao_input = QLineEdit()
        self.descricao_input.setPlaceholderText("")
        descricao_layout.addWidget(descricao_label)
        descricao_layout.addWidget(self.descricao_input)

        # endereco
        endereco_layout = QHBoxLayout()
        endereco_label = QLabel("Endereço:")
        self.endereco_input = QLineEdit()
        self.endereco_input.setPlaceholderText("")
        endereco_layout.addWidget(endereco_label)
        endereco_layout.addWidget(self.endereco_input)

        # botao de salvar
        salvar_botao = QPushButton("Salvar")
        # salvar_botao.clicked.connect()

        # status de salvar a loja
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adiciona os widgets de entrada ao layout do formulario
        form_layout.addWidget(titulo_label)
        form_layout.addLayout(nome_layout)
        form_layout.addLayout(descricao_layout)
        form_layout.addLayout(endereco_layout)
        form_layout.addWidget(salvar_botao)
        form_layout.addWidget(self.status_label)

        # Adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)

