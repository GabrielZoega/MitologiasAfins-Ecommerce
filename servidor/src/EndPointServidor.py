from ControladoraServidor import ControladoraServidor
import socket
import threading

# Essa será a classe responsável por receber as requisições dos clientes
class EndPointServidor:
    
    def __init__(self, host="0.0.0.0", porta=3000):
        self.host = host
        self.porta = porta
    
    def iniciaServidor(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((self.host, self.porta))
        servidor.listen()
        print(f"Servidor ouvindo em: {self.host}:{self.porta}")
        
        while True:
            socketCliente, addr = servidor.accept()
            print(f"Conexão de: {addr}")
            
            controladora = ControladoraServidor(socketCliente, addr)
            thread = threading.Thread(target=controladora.executa)
            thread.start()
    
if __name__ == "__main__":
    server = EndPointServidor()
    server.iniciaServidor()
        