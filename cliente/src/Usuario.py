from TipoCliente import TipoCliente
from Carrinho import Carrinho

class Usuario():
    def __init__(self):
        self.idUser = None
        self.nome = None
        self.email = None
        self.senha = None
        self.idCarrinho = None
        self.idLoja = None
        self.tipoCliente = TipoCliente.COMPRADOR
        
    def cadastrarUsuario(self, idUser: int, nome:str, email:str, senha:str, idCarrinho:int, tipoCliente:TipoCliente):
        print(f"\nCadastrando usuario: {nome} - {email} - {senha} - {idCarrinho} - {tipoCliente}\n")
        self.idUser = idUser
        self.nome = nome
        self.email = email
        self.senha = senha
        self.idCarrinho = idCarrinho
        self.tipoCliente = tipoCliente
        
    def fazerLogin(self, idUsuario: int, nome: str, email: str, senha: str, idCarrinho: int, idLoja: int, tipoCliente: TipoCliente):
        self.idUser = idUsuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.idCarrinho = idCarrinho
        self.idLoja = idLoja
        self.tipoCliente = tipoCliente
    