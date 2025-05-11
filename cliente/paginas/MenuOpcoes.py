from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt

class MenuOpcoes(QWidget):
    def __init__(self, paginas: QStackedWidget):
        super().__init__()
        self.paginas = paginas
        self.criaMenu()
    
    def criaMenu(self):

        main_layout = QVBoxLayout()

        # opcoes do menu
        categoria1 = QPushButton("Mitologia Egípcia")
        # categoria1.clicked.connect()

        categoria2 = QPushButton("Folclore Brasileiro")
        # categoria2.clicked.connect()

        categoria3 = QPushButton("Mitologia Grega")
        # categoria3.clicked.connect()

        main_layout.addWidget(categoria1)
        main_layout.addWidget(categoria2)
        main_layout.addWidget(categoria3)

        self.setLayout(main_layout)