class Produto():
    def __init__(self, idProduto:int, nome:str, descricao:str, preco:float, estoque:int, idLoja: int):
        self.idProduto = idProduto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.idLoja = idLoja

    def alterarNome(self,nome:str):
        self.nome = nome
        
    def alterarDescricao (self,descricao: str):
        self.descricao = descricao
    
    def alterarPreco (self,preco:float):
        self.preco = preco
        
    def alterarEstoque (self,estoque:int):
        self.estoque = estoque    
        