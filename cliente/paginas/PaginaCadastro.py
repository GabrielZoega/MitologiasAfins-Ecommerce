from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

class PaginaCadastro(QWidget):
    def __init__(self):
        super().__init__()

        self.criaPagina()
        

    def criaPagina(self):
        # Layout principal horizontal
        main_layout = QHBoxLayout()

        # Adiciona um espaço na esquerda para centralizar horizontalmente
        main_layout.addStretch(1)

        # Layout para o formulario 
        form_layout = QVBoxLayout() 

        # titulo do formulario
        titulo_label = QLabel("Faça seu Cadastro:")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # nome
        nome_layout = QHBoxLayout()
        nome_label = QLabel("Nome:")
        self.nome_input = QLineEdit()
        nome_layout.addWidget(nome_label)
        nome_layout.addWidget(self.nome_input)

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

        # botao de cadastro
        cadastro_botao = QPushButton("Cadastrar")
        cadastro_botao.clicked.connect(self.confere_cadastro)

        # status do login
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adiciona os widgets de entrada ao layout do formulario
        form_layout.addWidget(titulo_label)
        form_layout.addLayout(nome_layout)
        form_layout.addLayout(email_layout)
        form_layout.addLayout(senha_layout)
        form_layout.addWidget(cadastro_botao)
        form_layout.addWidget(self.status_label)

        # Adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)

        # Adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)

    def confere_cadastro(self):
        return