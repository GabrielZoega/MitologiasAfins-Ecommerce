from Anuncio import Anuncio
from Produto import Produto


class Loja():
    def __init__(self, idLoja: int, idUser: int ,nome:str ,endereco:str ,descricao:str):
        self.idLoja = idLoja
        self.idUsuario = idUser
        self.nome = nome
        self.endereco = endereco
        self.descricao = descricao
        self.anuncios = []
        self.produtos = []
        
    def alterarNome(self,nome:str):
        self.nome = nome
        
    def alterarEndereco (self,endereco:str):
        self.endereco = endereco
    
    def alterarDescricao (self,descricao:str):
        self.descricao = descricao
    
    def alterarAnuncio (self, idAnuncio:int, funcaoASerChamada:str, oQueAltera:str):
        for anuncio in self.anuncios:
            if anuncio.idAnuncio == idAnuncio:
               anuncio.alterarAnuncio(funcaoASerChamada, oQueAltera) 

    def alterarProduto (self, idProduto:int, funcaoASerChamada:str, oQueAltera:str):
        for produto in self.produtos:
            if produto.idProduto == idProduto:
                if funcaoASerChamada == "alterarNome":
                    produto.alterarNome(oQueAltera)
                elif funcaoASerChamada == "alterarDescricao":
                    produto.alterarDescricao (oQueAltera)
                elif funcaoASerChamada == "alterarPreco":
                    produto.alterarPreco (oQueAltera)
                else:
                    produto.alterarEstoque(oQueAltera)
    
    def excluirLoja(self):
        self.idLoja = None
        self.nome = None
        self.endereco = None
        self.descricao = None
        self.anuncios = []
        
    def excluirAnuncio(self,idAnuncio:int):
        for anuncio in self.anuncios:
            if(anuncio.idAnuncio == idAnuncio):
                self.anuncios.remove(anuncio)
                
    def excluirProduto (self,idProduto:int):
        for produto in self.produtos:
            if produto.idProduto == idProduto:
                self.produtos.remove(produto)
            for anuncio in self.anuncios:    
                if anuncio.idProduto == idProduto:
                    self.excluirAnuncio(anuncio.idAnuncio)