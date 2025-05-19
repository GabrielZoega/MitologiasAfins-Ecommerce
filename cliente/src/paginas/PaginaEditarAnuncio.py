import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ControladoraCliente import *

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QComboBox, QCheckBox, QVBoxLayout, QSpinBox, QDoubleSpinBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt
from ControladoraCliente import *
from Categoria import Categoria
from Anuncio import Anuncio
from Produto import Produto
from Status import Status


class PaginaEditarAnuncio(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente, anuncio: Anuncio, produto: Produto):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.anuncio = anuncio
        self.produto = produto
        self.cliente.categoria_anuncio_alterada.connect(self.respostaAlteracaoCategoria)
        self.cliente.visibilidade_anuncio_alterada.connect(self.respostaAlteracaoStatus)
        self.cliente.nome_produto_alterado.connect(self.respostaAlteracaoNomeProduto)
        self.cliente.descricao_produto_alterada.connect(self.respostaAlteracaoDescricaoProduto)
        self.cliente.preco_produto_alterado.connect(self.respostaAlteracaoPrecoProduto)
        self.cliente.estoque_produto_alterado.connect(self.respostaAlteracaoEstoqueProduto)
        self.cliente.anuncio_excluido.connect(self.respostaExclusaoAnuncio)
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
        titulo_label = QLabel("Edite seu anúncio:")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # categoria
        categoria_layout = QHBoxLayout()
        categoria_label = QLabel("Categoria:")
        self.categoria_input = QComboBox()
        self.categoria_input.addItems([categoria.value for categoria in Categoria])
        categoria_layout.addWidget(self.categoria_input)

        # visibilidade
        self.visibilidade_checkbox = QCheckBox("Ativo")
        self.visibilidade_checkbox.setChecked(True)

        # titulo do formulario de produto
        titulo_produto_label = QLabel("Edite seu produto:")
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
        salvar_botao = QPushButton("Salvar")
        salvar_botao.clicked.connect(self.alteraAnuncio)

        # status de salvar 
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        excluir_botao = QPushButton("Excluir")
        excluir_botao.clicked.connect(self.excluirAnuncioEProduto)
        excluir_botao.setStyleSheet("background-color: red;")

        # Adiciona os widgets ao layout do formulario
        # wigets de anuncio
        form_layout.addWidget(excluir_botao)
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
        form_layout.addWidget(self.status_label)

        # Adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)


    def alteraAnuncio(self):
        categoria = self.categoria_input.currentText()
        visibilidade = Status.ATIVO if self.visibilidade_checkbox.isChecked() else Status.PAUSADO
        nome = self.nome_input.text()
        descricao = self.descricao_input.text()
        preco = self.preco_input.value()
        estoque = self.estoque_input.value()
        
        print(f"Visibilidade: {visibilidade} Status: {self.anuncio.status}")
        print(f"Categoria: {Categoria(categoria)} Categoria: {self.anuncio.categoria}")

        if Categoria(categoria) != Categoria[self.anuncio.categoria]:
            self.cliente.alterarCategoria(idAnuncio=self.anuncio.idAnuncio, categoria=Categoria(categoria))
        if visibilidade != self.anuncio.status:
            self.cliente.alterarStatus(idAnuncio=self.anuncio.idAnuncio, status=visibilidade)
        if nome != self.produto.nome and nome != "":
            self.cliente.alterarNomeProduto(idProduto=self.produto.idProduto, nome=nome)
        if descricao != self.produto.descricao and descricao != "":
            self.cliente.alterarDescricaoProduto(idProduto=self.produto.idProduto, descricaoProduto=descricao)
        if preco != self.produto.preco:
            self.cliente.alterarPrecoProduto(idProduto=self.produto.idProduto, preco=preco)
        if estoque != self.produto.estoque:
            self.cliente.alterarEstoqueProduto(idProduto=self.produto.idProduto, estoque=estoque)
        

    def setAnuncio(self, anuncio: Anuncio):
        self.anuncio = anuncio
        print("Categoria: ", Categoria[anuncio.categoria].value)
        self.categoria_input.setCurrentText(Categoria[anuncio.categoria].value)
        print("Visibilidade: ", anuncio.status)
        self.visibilidade_checkbox.setChecked(anuncio.status == Status.ATIVO)

    def setProduto(self, produto: Produto):
        self.produto = produto
        self.nome_input.setPlaceholderText(produto.nome)
        self.descricao_input.setPlaceholderText(produto.descricao)
        self.preco_input.setValue(produto.preco)
        self.estoque_input.setValue(produto.estoque)

    def respostaAlteracaoCategoria(self, categoria: str):
        print("Categoria at: ", Categoria(categoria).name)
        print("Anuncio at: ", self.anuncio.categoria)
        self.anuncio.categoria = Categoria(categoria).name
        self.categoria_input.setCurrentText(categoria)
        self.status_label.setText("Categoria alterada com sucesso.")
    
    def respostaAlteracaoStatus(self, status: str):
        status = Status[status]
        print("Status at: ", status)
        print("Anuncio at: ", self.anuncio.status)
        self.anuncio.status = status
        self.visibilidade_checkbox.setChecked(status == Status.ATIVO)
        self.status_label.setText("Status alterado com sucesso.")

    def respostaAlteracaoNomeProduto(self, nome: str):
        self.produto.nome = nome
        self.nome_input.clear()
        self.nome_input.setPlaceholderText(nome)
        self.status_label.setText("Nome do produto alterado com sucesso.")
    
    def respostaAlteracaoDescricaoProduto(self, descricao: str):
        self.produto.descricao = descricao
        self.descricao_input.clear()
        self.descricao_input.setPlaceholderText(descricao)
        self.status_label.setText("Descrição do produto alterada com sucesso.")

    def respostaAlteracaoPrecoProduto(self, preco: float):
        self.produto.preco = preco
        self.preco_input.setValue(preco)
        self.status_label.setText("Preço do produto alterado com sucesso.")

    def respostaAlteracaoEstoqueProduto(self, estoque: int):
        self.produto.estoque = estoque
        self.estoque_input.setValue(estoque)
        self.status_label.setText("Estoque do produto alterado com sucesso.")

    def excluirAnuncioEProduto(self):
        self.cliente.excluirAnuncio(idAnuncio=self.anuncio.idAnuncio)
        self.cliente.excluirProduto(idProduto=self.produto.idProduto)
        self.status_label.setText("Anúncio e produto excluídos com sucesso.")

    def respostaExclusaoAnuncio(self):
        self.status_label.setText("Anúncio excluído com sucesso.")
        self.paginas.setCurrentIndex(self.paginas.PAGINA_EDITAR_ANUNCIOS)
        self.cliente.recuperaAnuncios()
        self.cliente.recuperaProdutos()