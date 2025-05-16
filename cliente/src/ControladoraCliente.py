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
import threading

class ControladoraCliente():
    
    def __init__(self, host="127.0.0.1", porta=3000):
        self.host = host
        self.porta = porta
        self.loja = None
        self.carrinho = None
        self.usuario = None
        self.anuncios = [];
        self.resultado_pesquisa = [];
        self.sockFile = None
        
    def estabeleceConexao(self):
        for i in range (10): #Espera o sevidor iniciar
            try:
                with socket.create_connection((self.host, self.porta)) as sock:
                    sockFile = sock.makefile(mode='rw')
                    print("Conectado ao servidor")
                    self.sockFile = sockFile

                    self.thread_escuta = threading.Thread(target=self.escuta_servidor)
                    self.thread_escuta.start()

            except:
                print(f"Tentando conectar ao servidor, tentativa {i + 1}/10...")
                time.sleep(1)  # Espera 1 segundo antes de tentar novamente
    
    def escuta_servidor(self):
        

        while True:
            try:
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta do servidor: ", dados)
                    
                    match dados.get("comando"):
                        case "criarLoja":
                            idLoja = dados.get("idLoja")
                            nomeLoja = dados.get("nomeLoja")
                            descricaoLoja = dados.get("descricaoLoja")
                            endereco = dados.get("endereco")
                            self.loja = Loja(idLoja, self.usuario.idUser, nomeLoja, descricaoLoja, endereco)
                        case "criarAnuncio":
                            idProduto = dados.get("idProduto")
                            categoria = dados.get("categoria")
                            status = dados.get("status")
                            idAnuncio = dados.get("idAnuncio")
                            self.loja.anuncios.append(Anuncio(idProduto,categoria,status,idAnuncio))
                        case "criarProduto":
                            idProduto = dados.get("idProduto")
                            nomeProduto = dados.get("nomeProduto")
                            descricao = dados.get("descricao")
                            preco = dados.get("preco")
                            estoque = dados.get("estoque")
                            self.loja.produtos.append(Produto(idProduto,nomeProduto,descricao,preco,estoque))
                        case "cadastrarUsuario":
                            idUsuario = dados.get("idUsuario")
                            idCarrinho = dados.get("idCarrinho")
                            nome = dados.get("nome")
                            email = dados.get("email")
                            senha = dados.get("senha")
                            self.usuario.cadastrarUsuario(idUsuario,nome, email, senha, idCarrinho, TipoCliente.COMPRADOR)
                            self.carrinho = Carrinho(idCarrinho)
                        case "fazerLogin":
                            status = dados.get("status")
                            if status == "ok":
                                self.usuario.fazerLogin(status)
                            else:
                                print("Tentativa falha de login")
                        case "excluirLoja":
                            self.loja.excluirLoja()
                            self.loja = None
                        case "excluirAnuncio":
                            idAnuncio = dados.get("idAnuncio")
                            self.loja.excluirAnuncio(idAnuncio)
                        case "excluirProduto":
                            idProduto = dados.get("idProduto")
                            self.loja.excluirProduto(idProduto)
                        case "alterarNomeLoja":
                            nomeLoja = dados.get("nomeLoja")
                            self.loja.alterarNome(nomeLoja)
                        case "alterarEndereco":
                            endereco = dados.get("endereco")
                            self.loja.alterarEndereco(endereco)
                        case "alterarDescricaoLoja":
                            descricao = dados.get("descricao")
                            self.loja.alterarDescricao(descricao)
                        case "alterarCategoria":
                            idAnuncio = dados.get("idAnuncio")
                            categoria = dados.get("categoria")
                            for anuncios in self.loja.anuncios:
                                if idAnuncio == anuncios.idAnuncio:
                                    anuncios.alterarCategoria(categoria)
                        case "alterarStatus":
                            idAnuncio = dados.get("idAnuncio")
                            status = dados.get("status")
                            for anuncios in self.loja.anuncios:
                                if idAnuncio == anuncios.idAnuncio:
                                    anuncios.alterarStatus(status)
                        case "alterarProduto":
                            idAnuncio = dados.get("idAnuncio")
                            idProduto = dados.get("idProduto")
                            for anuncios in self.loja.anuncios:
                                if idAnuncio == anuncios.idAnuncio:
                                    anuncios.alterarIdProduto(idProduto)
                        case "alterarNomeProduto":
                            idProduto = dados.get("idProduto")
                            nome = dados.get("nome")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarNome(nome)
                        case "alterarDescricaoProduto":
                            idProduto = dados.get("idProduto")
                            descricaoProduto = dados.get("descricao")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarDescricao(descricaoProduto)
                        case "alterarPreco":
                            idProduto = dados.get("idProduto")
                            preco = dados.get("preco")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarPreco(preco)
                        case "alterarEstoque":
                            idProduto = dados.get("idProduto")
                            estoque = dados.get("estoque")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarEstoque(estoque)
                        case "adicionarItem":
                            idItem = dados.get("idItem")
                            precoProduto = dados.get("preco")
                            idProduto = dados.get("idProduto")
                            quantidade = dados.get("quantidade")
                            self.carrinho.adicionarItem(idProduto,precoProduto,quantidade, idItem)
                        case "alterarQuantidade":
                            idItem = dados.get("idItem")
                            quantidade = dados.get("quantidade")
                            self.carrinho.alterarQuantidade(quantidade,idItem)
                        case "fecharCarrinho":
                            codigo = dados.get("codigo")
                            if codigo == 200:
                                self.carrinho.fecharCarrinho()
                            else:
                                print("Não é possível fechar esse carrinho")
                        case "recuperaAnuncios":
                            qntAnuncios = dados.get("qntAnuncio")
                            idsAnuncio = dados.get("idsAnuncio")
                            categorias = dados.get("categorias")
                            status = dados.get("status")
                            idsProduto = dados.get("idsProduto")
                            idsLoja = dados.get("idsLoja")
                            
                            self.anuncios.clear()
                            for i in range (qntAnuncios):
                                anuncio = Anuncio(idsProduto[i], categorias[i], status[i], idsAnuncio[i], idsLoja[i])
                                self.anuncios.append(anuncio)
                            
                        case _:
                            print("Comando desconhecido recebido do servidor.")
                    
            except Exception as e:
                print(f"Erro ao escutar o servidor: {e}")
                break

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
            
    def cadastrarUsuario(self,nome:str,email:str,senha:str):
        try:
            payload = {
                "comando": "cadastrarUsuario",
                "parametros": {
                    "nome": nome,
                    "email": email,
                    "senha": senha
                    }
                }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       
            resposta = self.sockFile.readline()
            if resposta:
                dados = json.loads(resposta)
                print("Resposta: ", dados)
                idUsuario = dados.get("idUsuario")
                idCarrinho = dados.get("idCarrinho")
                self.usuario.cadastrarUsuario(idUsuario,nome, email, senha, idCarrinho, TipoCliente.COMPRADOR) #Verificar se está certo essa passagem de parâmetro
                self.carrinho = Carrinho(idCarrinho)
        except Exception as e:
            print(f"\n Erro: {e}")
        
    def fazerLogin(self,idUser:int, email: str, senha:str):
        try:
            payload = {
                "comando": "fazerLogin",
                "payload":{
                    "idUser":idUser,
                    "email":email,
                    "senha": senha
                }
            }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       
            resposta = self.sockFile.readline()
            if resposta:
                dados = json.loads(resposta)
                print("Resposta: ", dados)
                status = dados.get("status")
                self.usuario.fazerLogin (status)
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
    
    def alterarDescricaoProduto(self, idProduto:int, descricaoProduto: str):
            try:
                payload = {
                    "comando": "alterarDescricaoProduto",
                    "parametros" :{
                        "idProduto": idProduto,
                        "descricao":descricaoProduto
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
                            produtos.alterarDescricao(descricaoProduto)
            except Exception as e:
                print(f"\n Erro: {e}")

    def alterarPrecoProduto (self, idProduto:int, preco:float):
            try:
                payload = {
                    "comando": "alterarPreco",
                    "parametros" :{
                        "idProduto": idProduto,
                        "preco": preco
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
                            produtos.alterarPreco(preco)
            except Exception as e:
                print(f"\n Erro: {e}")        
                
    def alterarEstoqueProduto (self,idProduto:int, estoque: int):
            try:
                payload = {
                    "comando": "alterarEstoque",
                    "parametros" :{
                        "idProduto": idProduto,
                        "estoque": estoque
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
                            produtos.alterarEstoque(estoque)
            except Exception as e:
                print(f"\n Erro: {e}")
                
    def adcionarItem(self,idCarrinho:int,idProduto:int,quantidade:int):
            try:
                payload = {
                    "comando": "adicionarItem",
                    "parametros" :{
                        "idCarrinho": idCarrinho,
                        "idProduto": idProduto,
                        "quantidade": quantidade
                    }  
            }   
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    idItem = dados.get("idItem")
                    precoProduto = dados.get("preco")
                    self.carrinho.adicionarItem(idProduto,precoProduto,quantidade, idItem)
            except Exception as e:
                print(f"\n Erro: {e}")
    
    def alterarQuantidade(self,idItem:int, quantidade:int):
            try:
                payload = {
                    "comando": "alterarQuantidade",
                    "parametros" :{
                        "idItem": idItem,
                        "quantidade": quantidade
                    }  
            }   
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    self.carrinho.alterarQuantidade(quantidade,idItem)
            except Exception as e:
                print(f"\n Erro: {e}")        
    
    def fecharCarrinho(self, idCarrinho):
            try:
                payload = {
                    "comando": "fecharCarrinho",
                    "parametros" :{
                        "idItem": idCarrinho
                    }  
            }   
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       
                resposta = self.sockFile.readline()
                if resposta:
                    dados = json.loads(resposta)
                    print("Resposta: ", dados)
                    codigo = dados.get("codigo")
                    if codigo == 200:
                        self.carrinho.fecharCarrinho()
                    else:
                        print("Não é possível fechar esse carrinho")
            except Exception as e:
                print(f"\n Erro: {e}")       
                      
    def recuperaAnuncios (self):
        try:
            payload = {
                "comando": "recuperaAnuncios"
            }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       
            resposta = self.sockFile.readline()
            if resposta:
                dados = json.loads(resposta)
                print("Resposta: ", dados)
                anuncios = dados.get("anuncios")
                return anuncios
        except Exception as e:
            print(f"\n Erro: {e}") 