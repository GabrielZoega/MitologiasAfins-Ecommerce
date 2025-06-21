import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt
from ControladoraCliente import ControladoraCliente

class PaginaLogin(QWidget):
    def __init__(self, paginas: QStackedWidget, cliente: ControladoraCliente):
        super().__init__()
        self.paginas = paginas
        self.cliente = cliente
        self.cliente.login_validado.connect(self.responde_login)
        self.criaPagina()
        

    def criaPagina(self):
        # layout principal horizontal
        main_layout = QHBoxLayout()

        # adiciona um espaço na esquerda para centralizar horizontalmente
        main_layout.addStretch(1)

        # layout para o formulario 
        form_layout = QVBoxLayout()     

        # titulo do formulario
        titulo_label = QLabel("Faça o Login:")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # email
        email_layout = QHBoxLayout()
        email_label = QLabel("E-mail:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)

        # senha
        senha_layout = QHBoxLayout()
        senha_label = QLabel("Senha:")
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        senha_layout.addWidget(senha_label)
        senha_layout.addWidget(self.senha_input)

        # botao de login
        login_botao = QPushButton("Login")
        login_botao.clicked.connect(self.confere_login)

        # label de cadastro
        cadastro_label = QLabel("Não possui cadastro?")
        cadastro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # botao de cadastro
        cadastro_botao = QPushButton("Cadastrar")
        cadastro_botao.clicked.connect(lambda: self.paginas.setCurrentIndex(self.paginas.PAGINA_CADASTRO))

        # status do login
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # adiciona os widgets de entrada ao layout do formulario
        form_layout.addWidget(titulo_label)
        form_layout.addLayout(email_layout)
        form_layout.addLayout(senha_layout)
        form_layout.addWidget(login_botao)
        form_layout.addWidget(cadastro_label)
        form_layout.addWidget(cadastro_botao)
        # adiciona o label de status
        form_layout.addWidget(self.status_label)

        # adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)

        # adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)

    def confere_login(self):
        self.status_label.setText("Tentando fazer login...")
        print(self.email_input.text(), self.senha_input.text())
        self.cliente.fazerLogin(self.email_input.text(), self.senha_input.text())

    def responde_login(self, sucesso: bool, mensagem: str):
        self.status_label.setText(mensagem)
        if sucesso:
            self.cliente.recuperaAnuncios()
            self.cliente.recuperaProdutos()
            self.cliente.recuperaCarrinho(self.cliente.usuario.idUser)
            self.cliente.recuperaItens(self.cliente.usuario.idCarrinho)
            self.paginas.setCurrentIndex(self.paginas.PAGINA_INICIAL)
            if self.cliente.usuario.idLoja is not None:
                print(f"Recuperando loja -> {self.cliente.usuario.idLoja}")
                self.cliente.recuperaLoja(self.cliente.usuario.idLoja)
                self.cliente.recuperaAnunciosUser(self.cliente.usuario.idLoja)
                print("Recuperando produtos da loja 1")
                self.cliente.recuperaProdutosUser(self.cliente.usuario.idLoja)
        else:
            return