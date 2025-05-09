class Anuncio():
    def __init__(self, idProduto, categoria, status, idAnuncio):
        self.idProduto = idProduto # Não é produto para facilitar na hora de fazer exclusão
        self.categoria = categoria
        self.status = status
        self.idAnuncio = idAnuncio
        
    def alterarIdProduto(self,produto):
        self.produto = produto
        
    def alterarCategoria(self,categoria):
        self.categoria = categoria
        
    def alterarStatus (self,status):
        self.status = status
    
    def alterarAnuncio(self, nomeOperacao, oQueAlterar):
        if(nomeOperacao == "alterarIdProduto"):
            self.alterarProduto(oQueAlterar)
        elif (nomeOperacao == "alterarCategoria"):
            self.alterarCategotia(oQueAlterar)
        else:
            self.alterarStatus(oQueAlterar)


        