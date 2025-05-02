import sqlite3

class AcessoBanco:
    
    def __init__(self):
        self.cur = self.iniciaBanco()
    
    def iniciaBanco():
        # Criando o arquivo do database para testes
        con = sqlite3.connect('/data/maSql.db')
        # Roda o arquivo init com as tabelas a serem criadas
        with open('/data/init.sql') as f:
            con.executescript(f.read())
        con.commit()
        # Talvez retornar esse con, dessa forma ele fica na classe e pode ser usado em outros lugares
        return con.cursor()
    
    def getCur(self):
        return self.cur