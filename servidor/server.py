import socket
import sqlite3


HOST = "0.0.0.0"  
PORT = 6600      

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Conexão recebida de {addr}")

        nome = conn.recv(1024).decode()
        if not nome:
            break
        
        # Criando o arquivo do database para testes
        con = sqlite3.connect('/data/maSql.db')
        # Roda o arquivo init com as tabelas a serem criadas
        with open('/data/init.sql') as f:
            con.executescript(f.read())
        con.commit()
        
        #cursos para acessar o banco
        cur = con.cursor()
        
        cur.execute('SELECT nome FROM usuario WHERE id = 1')
        # é necessário usar o fetch para recuperar as informações (fetchone() pega o primeiro da pilha)
        teste = cur.fetchone()
        
        # Aqui deve coloquei pra responder o nome do banco só pra testar
        resposta = f"roi {teste[0]}, né?"
        conn.sendall(resposta.encode())

        conn.close()

if __name__ == "__main__":
    main()
