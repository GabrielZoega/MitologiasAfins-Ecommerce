import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QToolBar, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
from PyQt6.QtGui import QColor, QPalette, QAction

from paginas.PaginaLogin import *
from paginas.PaginaCadastro import *
from paginas.PaginaInicial import *

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mitologias&Afins")
        self.resize(QSize(960, 540))
        
        self.setStyleSheet("background-color: #323031; color: #E2E2E2")

        # adiciona a barra de ferramentas
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.addToolBar(toolbar)

        # botao para mudar o tema
        self.tema = {"modo": "Tema escuro"}
        self.action_mudar_tema = QAction(self.tema["modo"], self)
        self.action_mudar_tema.triggered.connect(lambda: self.mudaTema(tema=self.tema))
        toolbar.addAction(self.action_mudar_tema)

        self.paginas = QStackedWidget()

        # adiciona as paginas na pilha de widgets
        self.pagina_login = PaginaLogin(self.paginas)
        self.pagina_cadastro = PaginaCadastro()
        self.pagina_inicial = PaginaInicial(self.paginas)

        self.paginas.addWidget(self.pagina_login)       # 0
        self.paginas.addWidget(self.pagina_cadastro)    # 1
        self.paginas.addWidget(self.pagina_inicial)     # 2
        

        self.setCentralWidget(self.paginas)  
        self.paginas.setCurrentIndex(2)     
        
   

    def mudaTema(self, tema):
        if(tema["modo"] == "Tema escuro"):
            self.setStyleSheet("background-color: #BBBAC6; color: #323031")
            tema["modo"] = "Tema claro"
            
        else:
            self.setStyleSheet("background-color: #323031; color: #E2E2E2")
            tema["modo"] = "Tema escuro"

        self.action_mudar_tema.setText(tema["modo"])




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()