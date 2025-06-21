from Categoria import Categoria
from Status import Status
from AcessoBanco import AcessoBanco
from Produto import Produto

class Anuncio:
    
    def __init__(self, idProduto: int, idLoja: int,categoria: Categoria, status: Status):
        self.idAnuncio = 0
        self.idProduto = idProduto
        self.idLoja = idLoja
        self.categoria = categoria
        self.status = status