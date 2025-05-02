from Anuncio import Anuncio

class Loja:
    
    def __init__(self, nome: str, endereco: str, descricao: str):
        self.idLoja = 0
        self.nome = nome
        self.endereco = endereco
        self.descricao = descricao
        self.anuncios = []
        
    