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
        self.cliente.loja_recuperada.connect(self.respostaRecuperacaoLoja)
        self.cliente.nome_loja_alterado.connect(self.respostaAlteracaoNomeLoja)
        self.cliente.descricao_loja_alterada.connect(self.respostaAlteracaoDescricaoLoja)
        self.cliente.endereco_loja_alterado.connect(self.respostaAlteracaoEnderecoLoja)
        self.cliente.loja_excluida.connect(self.respostaExclusaoLoja)
        self.criaPagina()


    def criaPagina(self):
        # layout principal horizontal
        main_layout = QHBoxLayout()

        # adiciona um espaco na esquerda para centralizar horizontalmente
        # main_layout.addStretch(1)

        # layout para as opcoes de anuncio
        opcoes_layout = QVBoxLayout()

        # layout para o formulario 
        form_layout = QVBoxLayout() 

        # opcoes de anuncio
        gerenciar_anuncios_botao = QPushButton("Gerenciar Anúncios")
        gerenciar_anuncios_botao.clicked.connect(self.irParaGerenciarAnuncios)
        opcoes_layout.addWidget(gerenciar_anuncios_botao)

        # titulo do formulario
        titulo_label = QLabel("Edite sua loja:")
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

        # botao de salvar
        salvar_botao = QPushButton("Salvar")
        salvar_botao.clicked.connect(self.alteraLoja)

        # status de salvar a loja
        self.status_nome_label = QLabel("")
        self.status_nome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_descricao_label = QLabel("")
        self.status_descricao_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_endereco_label = QLabel("")
        self.status_endereco_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        excluir_botao = QPushButton("Excluir")
        excluir_botao.clicked.connect(self.excluirLoja)
        excluir_botao.setStyleSheet("background-color: red;")

        # Adiciona os widgets de entrada ao layout do formulario
        form_layout.addWidget(excluir_botao)
        form_layout.addWidget(titulo_label)
        form_layout.addLayout(nome_layout)
        form_layout.addLayout(descricao_layout)
        form_layout.addLayout(endereco_layout)
        form_layout.addWidget(salvar_botao)
        form_layout.addWidget(self.status_nome_label)
        form_layout.addWidget(self.status_descricao_label)
        form_layout.addWidget(self.status_endereco_label)

        # Adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)
        main_layout.addLayout(opcoes_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        # main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)


    def alteraLoja(self):
        nome = self.nome_input.text()
        descricao = self.descricao_input.text()
        endereco = self.endereco_input.text()

        if not nome and not descricao and not endereco:
            self.status_label.setText("Preencha alguma informação para editar a loja")
            return
        
        if nome != "":
            self.cliente.alterarNomeLoja(nome)
        if descricao != "":
            self.cliente.alterarDescricaoLoja(descricao)
        if endereco != "":
            self.cliente.alterarEndereco(endereco)

    def respostaRecuperacaoLoja(self, nome: str, descricao: str, endereco: str):
        self.nome_input.setPlaceholderText(nome)
        self.descricao_input.setPlaceholderText(descricao)
        self.endereco_input.setPlaceholderText(endereco)

    def respostaAlteracaoNomeLoja(self, nome):
        self.nome_input.clear()
        self.nome_input.setPlaceholderText(nome)
        self.status_nome_label.setText("Nome da loja alterado com sucesso")

    def respostaAlteracaoDescricaoLoja(self, descricao):
        self.descricao_input.clear()
        self.descricao_input.setPlaceholderText(descricao)
        self.status_descricao_label.setText("Descrição da loja alterada com sucesso")

    def respostaAlteracaoEnderecoLoja(self, endereco):
        self.endereco_input.clear()
        self.endereco_input.setPlaceholderText(endereco)
        self.status_endereco_label.setText("Endereço da loja alterado com sucesso")

    def irParaGerenciarAnuncios(self):
        self.paginas.setCurrentIndex(self.paginas.PAGINA_EDITAR_ANUNCIOS)

    def excluirLoja(self):
        self.cliente.excluirLoja(self.cliente.loja.idLoja)
        self.cliente.usuario.idLoja = None

    def respostaExclusaoLoja(self):
        self.paginas.setCurrentIndex(self.paginas.PAGINA_CRIAR_LOJA)
        self.cliente.recuperaAnuncios()
        self.cliente.recuperaProdutos()