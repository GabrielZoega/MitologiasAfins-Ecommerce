from TipoCliente import TipoCliente

class Usuario():
    def __init__(self, nome:str, email:str, senha:str, idCarrinho:int, tipoCliente:TipoCliente):
        self.idUser = 0
        self.nome = nome
        self.email = email
        self.senha = senha
        self.idCarrinho = idCarrinho
        self.tipoCliente = tipoCliente
        
# Cadastrar usuário não seria só fazer ele passar pelo construtor?
    def CadastrarUsuario(self, idUser: int, nome:str, email:str, senha:str, idCarrinho:int, tipoCliente:TipoCliente):
        self.Usuario(nome, email, senha, idCarrinho, tipoCliente)
        self.idUser = idUser
        
    def fazerLogin(self, status:str):
        if (status == "ok"):
            print("Login efetuado com sucesso")
        else:
            print("Tentativa falha de login")
    