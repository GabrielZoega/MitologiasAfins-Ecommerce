from AcessoBanco import AcessoBanco

class Produto:
    
    def __init__(self, nome: str, descricao: str, preco: float, estoque: int):
        self.idProduto = 0
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
    
    def criarProdutoBanco(self, banco: AcessoBanco):
        banco.cur.execute("""
            INSERT INTO produto (nomeProduto, descricaoProduto, preco, estoque)
            VALUES (?, ?, ?, ?)
        """, (self.nome, self.descricao, self.preco, self.estoque))
        
        banco.cur.execute("SELECT idProduto FROM produto WHERE nomeProduto = ?", (self.nome))
        result = banco.cur.fetchone()
        self.idLoja = result[0]
        
        banco.con.commit()