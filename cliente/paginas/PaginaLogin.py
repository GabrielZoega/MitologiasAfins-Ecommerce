from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt

class PaginaLogin(QWidget):
    def __init__(self, paginas: QStackedWidget):
        super().__init__()
        self.paginas = paginas
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

        # status do login
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # adiciona os widgets de entrada ao layout do formulario
        form_layout.addWidget(titulo_label)
        form_layout.addLayout(email_layout)
        form_layout.addLayout(senha_layout)
        form_layout.addWidget(login_botao)
        form_layout.addWidget(self.status_label)

        # adiciona o layout do formulario ao layout principal
        main_layout.addLayout(form_layout)

        # adiciona um espaço na direita para centralizar o formulario horizontalmente
        main_layout.addStretch(1)

        # define o layout principal para o widget
        self.setLayout(main_layout)

    def confere_login(self):
        if self.email_input.text() == "teste@teste.com" and self.senha_input.text() == "senha":
            self.paginas.setCurrentIndex(2)  # Muda para a HomePage
        else:
            self.status_label.setText("Tente novamente")