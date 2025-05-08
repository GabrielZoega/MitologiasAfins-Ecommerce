class Anuncio():
    def __init__(self, produto, categoria, status, idAnuncio):
        self.produto = produto
        self.categoria = categoria
        self.status = status
        self.idAnuncio = idAnuncio
        
    def alterarProduto(self,produto):
        self.produto = produto
        
    def alterarCategoria(self,categoria):
        self.categoria = categoria
        
    def alterarStatus (self,status):
        self.status = status
    
    def alterarIdAnuncio (self,idAnuncio):
        self.idAnuncio = idAnuncio
        
    def alterarAnuncio(self, nomeOperacao, oQueAlterar):
        if(nomeOperacao == "alterarProduto"):
            self.alterarProduto(oQueAlterar)
        elif (nomeOperacao == "alterarCategoria"):
            self.alterarCategotia(oQueAlterar)
        elif (nomeOperacao == "alterarStatus"):
            self.alterarStatus(oQueAlterar)
        else:
            self.alterarIdAnuncio(oQueAlterar)