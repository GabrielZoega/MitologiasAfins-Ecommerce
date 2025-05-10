class Produto():
    def __init__(self, idProduto:int, nome:str, descricao:str, preco:float, estoque:int):
        self.idProduto = idProduto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque

    def alterarNome(self,nome):
        self.nome = nome
        
    def alterarDescricao (self,descricao):
        self.descricao = descricao
    
    def alterarPreco (self,preco):
        self.preco = preco
        
    def alterarEstoque (self,estoque):
        self.estoque = estoque    
        