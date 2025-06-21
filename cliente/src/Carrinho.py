from Item import Item

class Carrinho():
    def __init__(self,idCarrinho:int):
        self.itens = []
        self.idCarrinho = idCarrinho
        self.total = 0.0