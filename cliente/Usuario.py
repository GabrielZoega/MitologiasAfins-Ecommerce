from TipoCliente import TipoCliente

class Usuario():
    def __init__(self, nome, email, senha, carrinho, tipoCliente):
        self.idUser = 0
        self.nome = nome
        self.email = email
        self.senha = senha
        self.carrinho = carrinho
        self.tipoCliente = tipoCliente
    
#Fazer login -> tenho que mandar as informações para o servidor