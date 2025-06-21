from AcessoBanco import AcessoBanco

class Produto:
    
    def __init__(self, nome: str, descricao: str, preco: float, estoque: int, idLoja: int):
        self.idProduto = 0
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.idLoja = idLoja