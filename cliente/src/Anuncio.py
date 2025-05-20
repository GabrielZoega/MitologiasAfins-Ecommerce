from Produto import Produto
from Status import Status
from Categoria import Categoria

class Anuncio():
    def __init__(self, idProduto:int, categoria:Categoria, status: Status, idAnuncio:int, idLoja: int):
        self.idProduto = idProduto
        self.categoria = categoria
        self.status = status
        self.idAnuncio = idAnuncio
        self.idLoja = idLoja
        
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


        