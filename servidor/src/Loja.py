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