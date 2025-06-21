import sqlite3
from Categoria import Categoria
from Status import Status

caminhoBanco = 'database/maSql.db'
caminhoSql = 'database/init.sql'

class AcessoBanco:
    
    def __init__(self):
        self.iniciaBanco()
    
    def iniciaBanco(self):
        con = sqlite3.connect(caminhoBanco)
        # Roda o arquivo init com as tabelas a serem criadas
        with open(caminhoSql) as f:
            con.executescript(f.read())
        con.commit()
        con.close()

    
    def cadastrarUsuario(self, nome: str, email: str, senha: str, idCarrinho: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        try:
            print(f"Nome: {nome}, Email: {email}, Senha: {senha}, idCarrinho: {idCarrinho}")
            cur.execute("""
                INSERT INTO usuario (nomeUsuario, email, senha, FK_carrinho, tipoUsuario)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, email, senha, idCarrinho, 'COMPRADOR'))
            
            cur.execute("SELECT idUsuario FROM usuario WHERE nomeUsuario = ?", (nome,))
            fetch = cur.fetchone()
                
            con.commit()
            con.close()
            return fetch[0]
        
        except Exception as e:
            con.commit()
            con.close()
            raise e

    def recuperaLogin(self, email: str):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("SELECT idUsuario, nomeUsuario ,email, senha, tipoUsuario, FK_lojaUser, FK_carrinho, tipoUsuario FROM usuario WHERE email = ?", (email,))
        result = cur.fetchone()
        if result is None:
            print("RecuperaLogin: Nenhum resultado encontrado")
            return None
        idUsuario, nome ,email, senha, tipoUsuario, FK_lojaUser, FK_carrinho, tipoUsuario = result
    
        con.commit()
        con.close()
        return idUsuario, nome ,email, senha, tipoUsuario, FK_lojaUser, FK_carrinho, tipoUsuario

    def recuperaLoja(self, idLoja):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("SELECT nomeLoja, endereco, descricaoLoja FROM loja WHERE idLoja = ?", (idLoja,))
        resposta = cur.fetchone()
        if not resposta:
            return None, None, None
        nomeLoja, endereco, descricaoLoja = resposta
        
        con.commit()
        con.close()
        return nomeLoja, endereco, descricaoLoja

    def criarCarrinho(self):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("INSERT INTO carrinho (total) VALUES (?)", (0,))
        idCarrinho = cur.lastrowid
        
        con.commit()
        con.close()
        return idCarrinho

    def adicionarItem(self, idCarrinho: int, idProduto: int, quantidade: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        try:
            cur.execute("""
                INSERT INTO item (FK_idCarrinho, FK_produto, quantidade)
                VALUES (?, ?, ?)
            """, (idCarrinho, idProduto, quantidade))
            idItem = cur.lastrowid
            
            cur.execute("SELECT preco FROM produto WHERE idProduto = ?", (idProduto,))
            preco = cur.fetchone()
            preco = preco[0]
            
            cur.execute("SELECT total FROM carrinho WHERE idCarrinho = ?", (idCarrinho,))
            total = cur.fetchone()
            total = total[0]
            
            total += preco * quantidade
            cur.execute("UPDATE carrinho SET total = ? WHERE idCarrinho = ?", (total, idCarrinho))
            
            con.commit()
            con.close()
            return idItem
        
        except Exception as e:
            con.commit()
            con.close()
            raise e

    def alterarQuantidade(self, idItem: int, quantidade: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        if quantidade == 0:
            cur.execute("DELETE FROM item WHERE idItem = ?", (idItem,))
        else:
            cur.execute("UPDATE item SET quantidade = ? WHERE idItem = ?", (quantidade, idItem))
            
        con.commit()
        con.close()
    
    # Criar uma loja
    def criarLoja(self, nome: str, endereco: str, descricao: str, idUsuario: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO loja (nomeLoja, endereco, descricaoLoja)
                VALUES (?, ?, ?)
            """, (nome, endereco, descricao))
            
            cur.execute("SELECT idLoja FROM loja WHERE nomeLoja = ?", (nome,))
            result = cur.fetchone()
            idLoja = result[0]

            cur.execute("UPDATE usuario SET FK_lojaUser = ? WHERE idUsuario = ?", (idLoja, idUsuario))
            cur.execute("UPDATE usuario SET tipoUsuario = ? WHERE idUsuario = ?", ('VENDEDOR', idUsuario))
            
            con.commit()
            con.close()
            return idLoja
        
        except Exception as e:
            con.commit()
            con.close()
            raise e
            
    
    # Altere o nome da loja
    def alterarNomeLoja(self, nome: str, idLoja: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE loja SET nomeLoja = ? WHERE idLoja = ?", (nome, idLoja))
        con.commit()
        con.close()
        
    # Altere o endereco da loja
    def alterarEndereco(self, endereco: str, idLoja: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE loja SET endereco = ? WHERE idLoja = ?", (endereco, idLoja))
        con.commit()
        con.close()
        
    # Altere a descricao da loja
    def alterarDescricaoLoja(self, descricao: str, idLoja: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE loja SET descricaoLoja = ? WHERE idLoja = ?", (descricao, idLoja))
        con.commit()
        con.close()
    
    
    # Operações de Edição do Anuncio
    def alterarCategoria(self, idAnuncio: int, categoria: Categoria):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE anuncio SET categoria = ? WHERE idAnuncio = ?", (categoria.name, idAnuncio))
        con.commit()
        con.close()
        
    def alterarStatus(self, idAnuncio: int, status: str):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE anuncio SET statusAnuncio = ? WHERE idAnuncio = ?", (status, idAnuncio))
        con.commit()
        con.close()
    
    def alterarProduto(self, idAnuncio: int, idProduto: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE anuncio SET FK_idProduto = ? WHERE idAnuncio = ?", (idProduto, idAnuncio))
        con.commit()
        con.close()


    # Operações de Edição do Produto
    def alterarNomeProduto(self, idProduto: int, nome: str):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE produto SET nomeProduto = ? WHERE idProduto = ?", (nome, idProduto))
        con.commit()
        con.close()
            
    def alterarDescricaoProduto(self, idProduto: int, descricao: str):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE produto SET descricaoProduto = ? WHERE idProduto = ?", (descricao, idProduto))
        con.commit()
        con.close()
        
                
    def alterarPreco(self, idProduto: int, preco: float):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE produto SET preco = ? WHERE idProduto = ?", (preco, idProduto))
        con.commit()
        con.close()

                
    def alterarEstoque(self, idProduto: int, estoque: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE produto SET estoque = ? WHERE idProduto = ?", (estoque, idProduto))
        con.commit()
        con.close()
        
    
    # Exclui a loja e todos os seus anuncios e produtos
    def excluirLoja(self, idLoja: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("UPDATE usuario SET FK_lojaUser = NULL WHERE FK_lojaUser = ?", (idLoja,))
        cur.execute("UPDATE usuario SET tipoUsuario = ? WHERE FK_lojaUser = ?", ('COMPRADOR', idLoja))

        cur.execute("DELETE FROM loja WHERE idLoja = ?", (idLoja,))
        con.commit()
        con.close()
    
    # Exclui o Anuncio
    def excluirAnuncio(self, idAnuncio: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("DELETE FROM anuncio WHERE idAnuncio = ?", (idAnuncio,))
        con.commit()
        con.close()
    
    # Exclui o produto e seu respectivo anuncio
    def excluirProduto(self, idProduto: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        cur.execute("DELETE FROM produto WHERE idProduto = ?", (idProduto,))
        con.commit()
        con.close()

    # Cria um produto
    def criarProduto(self, nome: str, descricao: str, preco: float, estoque: int, idLoja: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        try:
            cur.execute("""
                INSERT INTO produto (nomeProduto, descricaoProduto, preco, estoque, FK_Loja)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, descricao, preco, estoque, idLoja))
            
            cur.execute("SELECT idProduto FROM produto WHERE nomeProduto = ?", (nome,))
            result = cur.fetchone()
            idProduto = result[0]
            
            con.commit()
            con.close()
            return idProduto
        
        except Exception as e:
            con.commit()
            con.close()
            raise e

    # Cria um anuncio
    def criarAnuncio(self, categoria: Categoria, status: Status, idProduto: int, idLoja: int):
        con = sqlite3.connect(caminhoBanco)
        cur = con.cursor()
        
        try:
            cur.execute("""
                INSERT INTO anuncio (categoria, statusAnuncio, FK_idProduto, FK_idLoja)
                VALUES (?, ?, ?, ?)
            """, (categoria, Status(1).name, idProduto, idLoja))
            
            cur.execute("SELECT idAnuncio FROM anuncio WHERE FK_idProduto = ?", (idProduto,))
            result = cur.fetchone()
            idAnuncio = result[0]
            
            con.commit()
            con.close()
            return idAnuncio
        
        except Exception as e:
            con.commit()
            con.close()
            raise e