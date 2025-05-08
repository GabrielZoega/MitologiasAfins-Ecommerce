from AcessoBanco import AcessoBanco

class Produto:
    
    def __init__(self, nome: str, descricao: str, preco: float, estoque: int, idLoja: int):
        self.idProduto = 0
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.idLoja = idLoja
    
    def criarProdutoBanco(self, banco: AcessoBanco):
        banco.cur.execute("""
            INSERT INTO produto (nomeProduto, descricaoProduto, preco, estoque, Fk_Loja)
            VALUES (?, ?, ?, ?, ?)
        """, (self.nome, self.descricao, self.preco, self.estoque, self.idLoja))
        
        banco.cur.execute("SELECT idProduto FROM produto WHERE nomeProduto = ?", (self.nome))
        result = banco.cur.fetchone()
        self.idLoja = result[0]
        
        banco.con.commit()
        
    def excluirProduto(self, banco: AcessoBanco):
        banco.cur.execute("DELETE FROM produto WHERE idProduto = ?", (self.idProduto,))
        banco.con.commit()