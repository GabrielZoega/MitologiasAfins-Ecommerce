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
    
    def criarAnuncioBanco(self, banco: AcessoBanco):
        banco.cur.execute("""
            INSERT INTO anuncio (categoria, statusAnuncio, FK_idProduto, FK_idLoja)
            VALUES (?, ?, ?, ?)
        """, (self.categoria, self.status, self.idProduto, self.idLoja))
        
        banco.cur.execute("SELECT idAnuncio FROM anuncio WHERE FK_idProduto = ?", (self.idProduto,))
        result = banco.cur.fetchone()
        self.idAnuncio = result[0]
        
        banco.con.commit()
        
    def excluirAnuncio(self, banco: AcessoBanco):
        banco.cur.execute("DELETE FROM anuncio WHERE idAnuncio = ?", (self.idAnuncio,))
        banco.con.commit()
    
    def alterarCategoria(self, categoria: Categoria, banco: AcessoBanco):
        print(f"Banco.alterarCategoria: {categoria}")
        banco.cur.execute("UPDATE anuncio SET categoria = ? WHERE idAnuncio = ?", (categoria.name, self.idAnuncio))
        banco.con.commit()
        
    def alterarStatus(self, status: Status, banco: AcessoBanco):
        banco.cur.execute("UPDATE anuncio SET status = ? WHERE idAnuncio = ?", (status.name, self.idAnuncio))
        banco.con.commit()

    def alterarProduto(self, idProduto: int, banco: AcessoBanco):
        banco.cur.execute("UPDATE anuncio SET FK_idProduto = ? WHERE idAnuncio = ?", (idProduto, self.idAnuncio))
        banco.con.commit()