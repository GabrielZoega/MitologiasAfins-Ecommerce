import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ControladoraCliente import ControladoraCliente

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QComboBox, QCheckBox, QVBoxLayout, QSpinBox, QDoubleSpinBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from Status import Status
from Categoria import Categoria

class PaginaCriarAnuncio(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.cliente.produto_criado.connect(self.respostaCriarProduto)
        self.cliente.anuncio_criado.connect(self.respostaCriarAnuncio)
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

        # titulo do formulario
        titulo_label = QLabel("Crie seu anúncio:")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # categoria
        categoria_layout = QHBoxLayout()
        categoria_label = QLabel("Categoria:")
        self.categoria_input = QComboBox()
        self.categoria_input.addItems([categoria.value for categoria in Categoria])
        categoria_layout.addWidget(categoria_label)
        categoria_layout.addWidget(self.categoria_input)

        # visibilidade
        self.visibilidade_checkbox = QCheckBox("Ativo")
        self.visibilidade_checkbox.setChecked(True)

        # titulo do formulario de produto
        titulo_produto_label = QLabel("Crie seu produto:")
        titulo_produto_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        # preco
        preco_layout = QHBoxLayout()
        preco_label = QLabel("Preço:")
        self.preco_input = QDoubleSpinBox()
        self.preco_input.setRange(0.0, 1000000.0)
        self.preco_input.setDecimals(2)
        self.preco_input.setSingleStep(0.5)
        self.preco_input.setPrefix("R$ ")
        self.preco_input.setValue(0.0)

        preco_layout.addWidget(preco_label)
        preco_layout.addWidget(self.preco_input)

        # estoque
        estoque_layout = QHBoxLayout()
        estoque_label = QLabel("Estoque:")
        self.estoque_input = QSpinBox()
        self.estoque_input.setRange(0, 1000000)
        self.estoque_input.setSingleStep(10)
        self.estoque_input.setValue(0)

        estoque_layout.addWidget(estoque_label)
        estoque_layout.addWidget(self.estoque_input)

        # botao de salvar
        salvar_botao = QPushButton("Criar")
        salvar_botao.clicked.connect(self.criaAnuncio)

        # status de salvar 

        # Adiciona os widgets ao layout do formulario
        # wigets de anuncio
        form_layout.addWidget(titulo_label)
        form_layout.addLayout(categoria_layout)
        form_layout.addWidget(self.visibilidade_checkbox)
        # widgets de produto
        form_layout.addWidget(titulo_produto_label)
        form_layout.addLayout(nome_layout)
        form_layout.addLayout(descricao_layout)
        form_layout.addLayout(preco_layout)
        form_layout.addLayout(estoque_layout)
        form_layout.addWidget(salvar_botao)

        # Adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)


    def criaAnuncio(self):
        self.cliente.criarProduto(nomeProduto=self.nome_input.text(), descricao=self.descricao_input.text(), preco=self.preco_input.value(),  estoque=self.estoque_input.value())
        
    def respostaCriarProduto(self, idProduto: str, mensagem: str):
        
        if idProduto != "-1":
            indice = self.categoria_input.currentIndex()

            categoria_nome = list(Categoria)[indice].name
            self.cliente.criarAnuncio(
                idProduto=idProduto,
                categoria=categoria_nome,
                status=Status.ATIVO if self.visibilidade_checkbox.isChecked() else Status.PAUSADO
            )
            self.cliente.recuperaProdutos()
        else:
            print(f"Erro: {mensagem}")

    def respostaCriarAnuncio(self, sucesso: str):
        if sucesso == "ok":
            self.paginas.setCurrentIndex(self.paginas.PAGINA_EDITAR_LOJA)
        else:
            print(sucesso)

        self.cliente.recuperaAnunciosUser(self.cliente.usuario.idUser)
