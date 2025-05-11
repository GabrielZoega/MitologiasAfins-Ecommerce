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
        self.cur.execute("""
            INSERT INTO usuario (nomeUsuario, email, senha, FK_carrinho)"
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha, idCarrinho))
        
        self.cur.execute("SELECT idUsuario FROM usuario WHERE nomeUsuario = ?", (nome,))
        fetch = self.cur.fetchone()        
        self.con.commit()
        return fetch[0]

    def recuperaLogin(self, idUser: int):
        self.cur.execute("SELECT email, senha FROM usuario WHERE idUsuario = ?", (idUser))
        result = self.cur.fetchone()
        self.con.commit()
        email, senha = result
        return email, senha

    def criarCarrinho(self):
        self.cur.execute("INSERT INTO carrinho (total) VALUES (?)", (0,))
        idCarrinho = self.cur.lastrowid
        self.con.commit()
        return idCarrinho

    def adicionarItem(self, idCarrinho: int, idProduto: int, quantidade: int):
        self.cur.execute("""
            INSERT INTO item (FK_idCarrinho, FK_produto, quantidade)"
            VALUES (?, ?, ?)
        """, (idCarrinho, idProduto, quantidade))
        
        idItem = self.cur.lastrowid      
        self.con.commit()
        return idItem

    def alterarQuantidade(self, idItem: int, quantidade: int):
        self.cur.execute("UPDATE item SET quantidade = ? WHERE idItem = ?", (quantidade, idItem))
        self.con.commit()