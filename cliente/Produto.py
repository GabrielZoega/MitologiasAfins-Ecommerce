class Produto():
    def __init__(self, idProduto, nome, descricao, preco, estoque):
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
        