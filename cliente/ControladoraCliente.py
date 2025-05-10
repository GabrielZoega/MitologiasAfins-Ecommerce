import socket
import json
import time
from Loja import Loja 
from Carrinho import Carrinho
from Item import Item
from Anuncio import Anuncio
from Categoria import Categoria
from Produto import Produto
from Status import Status
from TipoCliente import TipoCliente
from Usuario import Usuario

class ControladoraCliente():
    
    def __init__(self, host="127.0.0.1", porta=3000):
        self.host = host
        self.porta = porta
        self.loja = None
        self.usuario = None
        self.sockFile = None
        
    def estabeleceConexao(self):
        for i in range (10): #Espera o sevidor iniciar
            try:
                with socket.create_connection((self.host, self.porta)) as sock:
                    sockFile = sock.makefile(mode='rw')
                    print("Conectado ao servidor")
                    self.sockFile = sockFile
            except:
                print(f"Tentando conectar ao servidor, tentativa {i + 1}/10...")
                time.sleep(1)  # Espera 1 segundo antes de tentar novamente
    
    def criarLoja(self, nomeLoja: str, descricaoLoja: str, endereco: str):
        try:
            payload = {
                "comando": "criarLoja",
                "parametros": {
                    "nome": nomeLoja,
                    "descricao": descricaoLoja,
                    "endereco": endereco,
                    "idUsuario": self.usuario.idUser
                }
            }
        
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()
            
            resposta = self.sockFile.readline()
            if resposta:
                dados = json.loads(resposta)
                print("Resposta: ", dados)
                idLoja = dados.get("idLoja")
                self.loja = Loja(idLoja, self.usuario.idUser, nomeLoja, descricaoLoja, endereco)
        except Exception as e:
            print(f"\n Erro: {e}")
            
    def criarAnuncio(self, categoria:Categoria, status:Status, idProduto:int):
        try:
            payload = {
                "comando": "criarAnuncio",
                "parametros": {
                    "categoria": categoria,
                    "status": status,
                    "idLoja":self.loja.idLoja,
                    "idProduto": idProduto
                }
            }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       
            resposta = self.sockFile.readline()
            if resposta:
                dados = json.loads(resposta)
                print("Resposta: ", dados)
                idAnuncio = dados.get("idAnuncio")
                self.loja.anuncios.append(Anuncio(idProduto,categoria,status,idAnuncio))
        except Exception as e:
            print(f"\n Erro: {e}")
    
    def criarProduto(self, nomeProduto:str, descricao:str, preco:float, estoque:int):
        try:
            payload = {
                "comando": "criarProduto",
                "parametros": {
                    "nomeProduto": nomeProduto,
                    "descricao": descricao,
                    "preco": preco,
                    "estoque": estoque,
                    "idLoja": self.loja.idLoja
                }
            }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       
            resposta = self.sockFile.readline()
            if resposta:
                dados = json.loads(resposta)
                print("Resposta: ", dados)
                idProduto = dados.get("idProduto")
                self.loja.produtos.append(Produto(idProduto,nomeProduto,descricao,preco,estoque))
        except Exception as e:
            print(f"\n Erro: {e}")
    
    def excluirLoja(self):
            try:
                payload = {
                    "comando": "excluirLoja"   
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    self.loja.excluirLoja()
            except Exception as e:
                print(f"\n Erro: {e}")
    
    def excluirAnuncio(self,idAnuncio:int):
            try:
                payload = {
                    "comando": "excluirAnuncio",
                    "parametros" :{
                        "idAnuncio": idAnuncio    
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    self.loja.excluirAnuncio(idAnuncio)
                        
            except Exception as e:
                print(f"\n Erro: {e}")
                
    def excluirProduto(self,idProduto:int):
            try:
                payload = {
                    "comando": "excluirProduto",
                    "parametros" :{
                        "idProduto": idProduto    
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    self.loja.excluirProduto(idProduto)
            except Exception as e:
                print(f"\n Erro: {e}")

    def alterarNomeLoja(self,nomeLoja:str):
            try:
                payload = {
                    "comando": "alterarNomeLoja",
                    "parametros" :{
                        "nomeLoja": nomeLoja    
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    self.loja.alterarNome(nomeLoja)
            except Exception as e:
                print(f"\n Erro: {e}")

    def alterarEndereco(self,endereco:str):
            try:
                payload = {
                    "comando": "alterarendereco",
                    "parametros" :{
                        "endereco": endereco    
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    self.loja.alterarEndereco(endereco)
            except Exception as e:
                print(f"\n Erro: {e}")
            
    def alterarDescricaoLoja(self,descricao:str):
            try:
                payload = {
                    "comando": "alterarDescricaoLoja",
                    "parametros" :{
                        "descricao": descricao    
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    self.loja.alterarDescricao(descricao)
            except Exception as e:
                print(f"\n Erro: {e}")

    def alterarCategoria(self,idAnuncio:int, categoria: Categoria):
            try:
                payload = {
                    "comando": "alterarCategoria",
                    "parametros" :{
                        "idAnuncio": idAnuncio,
                        "categoria": categoria   
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    for anuncios in self.loja.anuncios:
                        if idAnuncio == anuncios.idAnuncio:
                            anuncios.alterarCategoria(categoria)
            except Exception as e:
                print(f"\n Erro: {e}")
   
    def alterarStatus(self,idAnuncio:int, status:Status):
            try:
                payload = {
                    "comando": "alterarStatus",
                    "parametros" :{
                        "idAnuncio": idAnuncio,
                        "status": status  
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    for anuncios in self.loja.anuncios:
                        if idAnuncio == anuncios.idAnuncio:
                            anuncios.alterarStatus(status)
            except Exception as e:
                print(f"\n Erro: {e}")         

    def alterarProduto(self,idAnuncio:int, idProduto:int):
            try:
                payload = {
                    "comando": "alterarProduto",
                    "parametros" :{
                        "idAnuncio": idAnuncio,
                        "idProduto": idProduto 
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    for anuncios in self.loja.anuncios:
                        if idAnuncio == anuncios.idAnuncio:
                            anuncios.alterarIdProduto(idProduto)
            except Exception as e:
                print(f"\n Erro: {e}") 

    def alterarNomeProduto(self, idProduto:int, nome: str):
            try:
                payload = {
                    "comando": "alterarNomeProduto",
                    "parametros" :{
                        "idProduto": idProduto,
                        "nome":nome
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    for produtos in self.loja.produtos:
                        if idProduto == produtos.idProduto:
                            produtos.alterarNome(nome)
            except Exception as e:
                print(f"\n Erro: {e}")