from Produto import Produto
from Categoria import Categoria
from Status import Status

class Anuncio:
    
    def __init__(self, produto: Produto, categoria: Categoria, status: Status):
        self.idAnuncio = 0
        self.produto = produto
        self.categoria = categoria
        self.status = status
    