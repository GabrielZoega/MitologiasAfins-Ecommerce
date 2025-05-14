from Produto import Produto
from Status import Status
from Categoria import Categoria

class Anuncio():
    def __init__(self, idProduto:int, categoria:Categoria, status: Status, idAnuncio:int):
        self.idProduto = idProduto # Não é produto para facilitar na hora de fazer exclusão
        self.categoria = categoria
        self.status = status
        self.idAnuncio = idAnuncio
        
    def alterarIdProduto(self,produto:int):
        self.produto = produto
        
    def alterarCategoria(self,categoria:Categoria):
        self.categoria = categoria
        
    def alterarStatus (self,status:Status):
        self.status = status
    
    def alterarAnuncio(self, nomeOperacao:str, oQueAlterar:str):
        if(nomeOperacao == "alterarIdProduto"):
            self.alterarProduto(oQueAlterar)
        elif (nomeOperacao == "alterarCategoria"):
            self.alterarCategoria(oQueAlterar)
        else:
            self.alterarStatus(oQueAlterar)


        