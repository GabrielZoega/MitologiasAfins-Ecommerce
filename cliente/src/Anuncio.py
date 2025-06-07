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