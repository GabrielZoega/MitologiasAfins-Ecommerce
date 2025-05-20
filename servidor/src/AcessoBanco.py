import sqlite3

class AcessoBanco:
    
    def __init__(self):
        self.con = self.iniciaBanco()
        self.cur = self.getCur()
    
    def iniciaBanco(self):
        # Criando o arquivo do database para testes
        con = sqlite3.connect('/data/maSql.db')
        # Roda o arquivo init com as tabelas a serem criadas
        with open('/data/init.sql') as f:
            con.executescript(f.read())
        con.commit()
        # Talvez retornar esse con, dessa forma ele fica na classe e pode ser usado em outros lugares
        return con
    
    def getCur(self):
        return self.con.cursor()
    
    def cadastrarUsuario(self, nome: str, email: str, senha: str, idCarrinho: int):
        print(f"Nome: {nome}, Email: {email}, Senha: {senha}, idCarrinho: {idCarrinho}")
        self.cur.execute("""
            INSERT INTO usuario (nomeUsuario, email, senha, FK_carrinho, tipoUsuario)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, email, senha, idCarrinho, 'COMPRADOR'))
        
        self.cur.execute("SELECT idUsuario FROM usuario WHERE nomeUsuario = ?", (nome,))
        fetch = self.cur.fetchone()        
        self.con.commit()
        return fetch[0]

    def recuperaLogin(self, email: str):
        self.cur.execute("SELECT idUsuario, nomeUsuario ,email, senha, tipoUsuario, FK_lojaUser, FK_carrinho FROM usuario WHERE email = ?", (email,))
        result = self.cur.fetchone()
        if result is None:
            print("RecuperaLogin: Nenhum resultado encontrado")
            return None
        self.con.commit()
        idUsuario, nome ,email, senha, tipoUsuario, FK_lojaUser, FK_carrinho = result
    
        return idUsuario, nome ,email, senha, tipoUsuario, FK_lojaUser, FK_carrinho

    def recuperaLoja(self, idLoja):
        self.cur.execute("SELECT nomeLoja, endereco, descricaoLoja FROM loja WHERE idLoja = ?", (idLoja,))
        resposta = self.cur.fetchone()
        if not resposta:
            return None, None, None
        nomeLoja, endereco, descricaoLoja = resposta
        
        return nomeLoja, endereco, descricaoLoja

    def criarCarrinho(self):
        self.cur.execute("INSERT INTO carrinho (total) VALUES (?)", (0,))
        idCarrinho = self.cur.lastrowid
        self.con.commit()
        return idCarrinho

    def adicionarItem(self, idCarrinho: int, idProduto: int, quantidade: int):
        self.cur.execute("""
            INSERT INTO item (FK_idCarrinho, FK_produto, quantidade)
            VALUES (?, ?, ?)
        """, (idCarrinho, idProduto, quantidade))
        idItem = self.cur.lastrowid
        
        self.cur.execute("SELECT preco FROM produto WHERE idProduto = ?", (idProduto,))
        preco = self.cur.fetchone()
        preco = preco[0]
        
        self.cur.execute("SELECT total FROM carrinho WHERE idCarrinho = ?", (idCarrinho,))
        total = self.cur.fetchone()
        total = total[0]
        
        total += preco * quantidade
        self.cur.execute("UPDATE carrinho SET total = ? WHERE idCarrinho = ?", (total, idCarrinho))
        
        self.con.commit()
        return idItem

    def alterarQuantidade(self, idItem: int, quantidade: int):
        if quantidade == 0:
            self.cur.execute("DELETE FROM item WHERE idItem = ?", (idItem,))
        else:
            self.cur.execute("UPDATE item SET quantidade = ? WHERE idItem = ?", (quantidade, idItem))
        self.con.commit()

