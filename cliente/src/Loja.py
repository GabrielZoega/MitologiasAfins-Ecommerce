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