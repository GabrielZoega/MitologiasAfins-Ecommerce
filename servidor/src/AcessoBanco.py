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
    
    def cadastrarUsuario(self, idUser: int, nome: str, email: str, senha: str):
        self.cur.execute("""
            INSERT INTO usuario (idUsuario, nomeUsuario, email, senha)"
            VALUES (? ? ? ?)
        """, (idUser, nome, email, senha))
        
    def recuperaLogin(self, idUser: int):
        self.cur.execute("SELECT email, senha FROM usuario WHERE idUsuario = ?", (idUser))
        result = self.cur.fetchone()
        email, senha = result
        return email, senha
        