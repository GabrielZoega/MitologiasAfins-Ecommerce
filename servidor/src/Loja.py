from AcessoBanco import AcessoBanco
from Anuncio import Anuncio
from Produto import Produto

class Loja:
    
    def __init__(self, nome: str, endereco: str, descricao: str, idUsuario: int):
        self.idLoja = 0
        self.nome = nome
        self.endereco = endereco
        self.descricao = descricao
        self.anuncios = []
        self.produtos = []
        self.idUsuario = idUsuario
    
    # Registra a loja no banco
    def criarLojaBanco(self, banco: AcessoBanco):
        banco.cur.execute("""
            INSERT INTO loja (nomeLoja, endereco, descricaoLoja)
            VALUES (?, ?, ?)
        """, (self.nome, self.endereco, self.descricao))
        
        banco.cur.execute("UPDATE usuario SET Fk_lojaUser = ? WHERE idUsuario = ?", (self.idLoja, self.idUsuario))
        
        banco.cur.execute("SELECT idLoja FROM loja WHERE nomeLoja = ?", (self.nome,))
        result = banco.cur.fetchone()
        self.idLoja = result[0]
        
        banco.con.commit()
    
    # Adiciona um anuncio na lista de anuncios da loja
    def adicionaAnuncio(self, anuncio: Anuncio):
        self.anuncios.append(anuncio)
    
    # Adiciona um produto na lista de produtos da loja
    def adicionaProduto(self, produto: Produto):
        self.produtos.append(produto)
    
    # Exclui a loja do banco
    def excluirLoja(self, banco: AcessoBanco):
        banco.cur.execute("DELETE FROM loja WHERE idLoja = ?", (self.idLoja,))
        banco.con.commit()
    
    # Altere o nome da loja no banco
    def alterarNomeLoja(self, nome: str, banco: AcessoBanco):
        banco.cur.execute("UPDATE loja SET nomeLoja = ? WHERE idLoja = ?", (nome, self.idLoja))
        banco.con.commit()
    
    # Altere o endereco da loja no banco
    def alterarEndereco(self, endereco: str, banco: AcessoBanco):
        banco.cur.execute("UPDATE loja SET endereco = ? WHERE idLoja = ?", (endereco, self.idLoja))
        banco.con.commit()
        
    # Altere a descricao da loja no banco
    def alterarDescricaoLoja(self, descricao: str, banco: AcessoBanco):
        banco.cur.execute("UPDATE loja SET descricaoLoja = ? WHERE idLoja = ?", (descricao, self.idLoja))
        banco.con.commit()
    