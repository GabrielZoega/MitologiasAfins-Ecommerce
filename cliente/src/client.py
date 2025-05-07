import socket
import json
import time

# HOST = "127.0.0.1"  
# PORT = 6600

# def enviar_nome(nome):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     print(f"Conectando ao servidor {HOST}:{PORT}...")

#     client.connect((HOST, PORT))
    
#     client.sendall(nome.encode())
#     resposta = client.recv(1024).decode()
    
#     client.close()
#     return resposta


def main():
    host = "127.0.0.1"
    porta = 3000
        
    for i in range (10):
        try:
            with socket.create_connection((host, porta)) as sock:
                sockFile = sock.makefile(mode='rw')
                print("Conectado ao servidor")
                break
        except:
            print(f"Tentando conectar ao servidor, tentativa {i + 1}/10...")
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
        
    try:
        while True:
            comando = "criarLoja"
            
            if comando == "sair":
                break
            
            if comando == "criarLoja":
                payload = {
                    "comando": "criarLoja",
                    "parametros": {
                        "nome": "nomeLoja",
                        "descricao": "descricaoLoja",
                        "endereco": "enderecoLoja",
                        "idUsuario": 5
                    }
                }
            
            sockFile.write(json.dumps(payload) + '\n')
            sockFile.flush()
            
            resposta = sockFile.readline()
            if resposta:
                dados = json.loads(resposta)
                print("Resposta: ", dados)
            break # só pra testar uma vez
    except KeyboardInterrupt:
        print("\n Encerrado pelo usuário")

if __name__ == "__main__":
    main()