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
from PyQt6.QtCore import QObject, pyqtSignal

class ControladoraCliente(QObject):
    
    login_validado = pyqtSignal(bool, str)
    anuncios_recuperados = pyqtSignal(list)
    produtos_recuperados = pyqtSignal(list)
    anuncios_user_recuperados = pyqtSignal(list)
    produtos_user_recuperados = pyqtSignal(list)
    loja_criada = pyqtSignal(bool)
    loja_recuperada = pyqtSignal(str, str, str)
    nome_loja_alterado = pyqtSignal(str)
    endereco_loja_alterado = pyqtSignal(str)
    descricao_loja_alterada = pyqtSignal(str)
    produto_criado = pyqtSignal(int)
    anuncio_criado = pyqtSignal(str)
    categoria_anuncio_alterada = pyqtSignal(str)
    visibilidade_anuncio_alterada = pyqtSignal(str)
    nome_produto_alterado = pyqtSignal(str)
    descricao_produto_alterada = pyqtSignal(str)
    preco_produto_alterado = pyqtSignal(float)
    estoque_produto_alterado = pyqtSignal(int)
    anuncio_excluido = pyqtSignal(str)
    loja_excluida = pyqtSignal(str)

    def __init__(self, host="127.0.0.1", porta=3000):
        super().__init__()
        self.host = host
        self.porta = porta
        self.loja = None
        self.carrinho = None
        self.usuario = Usuario()
        self.usuario.tipoCliente = TipoCliente.COMPRADOR
        self.anuncios = []
        self.produtos = []
        self.resultado_pesquisa = []
        self.sockFile = None
        
    def estabeleceConexao(self):
        for i in range (10): #Espera o sevidor iniciar
            try:
                if self.sockFile is not None:
                    break  # Já está conectado
                sock = socket.create_connection((self.host, self.porta))
                self.sockFile = sock.makefile(mode='rw')
                print("Conectado ao servidor")

                self.thread_escuta = threading.Thread(target=self.escuta_servidor, daemon=True)
                self.thread_escuta.start()
                break  # Sai do loop após conectar
            except Exception as e:
                print(f"Tentando conectar ao servidor, tentativa {i + 1}/10... {e}")
                time.sleep(1)
    
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
                            status = dados.get("status")
                            resposta = dados.get("resposta")


                            if status == "ok":
                                self.usuario.tipoCliente = TipoCliente.VENDEDOR
                                self.loja_criada.emit(True)
                            else:
                                self.loja_criada.emit(False)
                            print("Resposta: ", resposta)

                        case "criarAnuncio":
                            status = dados.get("status")
                            if status == "ok":
                                idProduto = dados.get("idProduto")
                                categoria = dados.get("categoria")
                                statusAnuncio = dados.get("statusAnuncio")
                                idAnuncio = dados.get("idAnuncio")
                                idLoja = dados.get("idLoja")
                                self.loja.anuncios.append(Anuncio(idProduto=idProduto,categoria=categoria,status=Status[statusAnuncio],idAnuncio=idAnuncio, idLoja=idLoja))
                            else:
                                print("Falha ao criar anúncio")
                            self.anuncio_criado.emit(status)

                        case "criarProduto":
                            idProduto = dados.get("idProduto")
                            nomeProduto = dados.get("nomeProduto")
                            descricao = dados.get("descricao")
                            preco = dados.get("preco")
                            estoque = dados.get("estoque")
                            idLoja = dados.get("idLoja")
                            self.loja.produtos.append(Produto(idProduto=idProduto,nome=nomeProduto,descricao=descricao,preco=preco,estoque=estoque,idLoja=idLoja))
                            self.produto_criado.emit(idProduto)
                            
                        case "cadastrarUsuario":
                            idUsuario = dados.get("idUsuario")
                            idCarrinho = dados.get("idCarrinho")
                            nome = dados.get("nome")
                            email = dados.get("email")
                            senha = dados.get("senha")
                            resposta = dados.get("resposta")
                            self.usuario.cadastrarUsuario(idUsuario,nome, email, senha, idCarrinho, TipoCliente.COMPRADOR)
                            self.carrinho = Carrinho(idCarrinho)
                            self.login_validado.emit(True, resposta)
                            
                        case "fazerLogin":
                            status = dados.get("status")
                            resposta = dados.get("resposta")
                            if status == "ok":
                                idUsuario = dados.get("idUsuario")
                                nome = dados.get("nome")
                                email = dados.get("email")
                                senha = dados.get("senha")
                                tipoCliente = dados.get("tipoCliente")
                                idLoja = dados.get("idLoja")
                                idCarrinho = dados.get("idCarrinho")
                                self.usuario.fazerLogin(idUsuario, nome, email, senha, idCarrinho, idLoja, TipoCliente[tipoCliente])
                                # self.recuperaCarrinho(idUsuario)
                                # self.recuperaItens(idCarrinho)
                                print(f"ID Loja: {idLoja}")
                                if idLoja is not None:
                                    print("Recuperando loja")
                                    self.recuperaLoja(idLoja, idUsuario)
                                    self.recuperaProdutosUser(idLoja)
                                    self.recuperaAnunciosUser(idLoja)
                                self.login_validado.emit(True, resposta)
                            else:
                                print("Tentativa falha de login")
                                self.login_validado.emit(False, resposta)

                        case "excluirLoja":
                            self.usuario.tipoCliente = TipoCliente.COMPRADOR
                            self.loja.excluirLoja()
                            self.loja = None
                            self.usuario.idLoja = None
                            self.loja_excluida.emit("Loja excluída com sucesso")
                            
                        case "excluirAnuncio":
                            idAnuncio = dados.get("idAnuncio")
                            self.loja.excluirAnuncio(idAnuncio)
                            self.anuncio_excluido.emit(idAnuncio)
                            
                        case "excluirProduto":
                            idProduto = dados.get("idProduto")
                            self.loja.excluirProduto(idProduto)
                            
                        case "alterarNomeLoja":
                            nomeLoja = dados.get("nomeLoja")
                            self.loja.alterarNome(nomeLoja)
                            self.nome_loja_alterado.emit(nomeLoja)
                            
                        case "alterarEndereco":
                            endereco = dados.get("endereco")
                            self.loja.alterarEndereco(endereco)
                            self.endereco_loja_alterado.emit(endereco)

                        case "alterarDescricaoLoja":
                            descricao = dados.get("descricao")
                            self.loja.alterarDescricao(descricao)
                            self.descricao_loja_alterada.emit(descricao)

                        case "alterarCategoria":
                            idAnuncio = dados.get("idAnuncio")
                            categoria = Categoria(dados.get("categoria"))
                            print(f"Categoria: {categoria}") 
                            for anuncios in self.loja.anuncios:
                                if idAnuncio == anuncios.idAnuncio:
                                    anuncios.alterarCategoria(categoria)
                            self.categoria_anuncio_alterada.emit(categoria.value)
                                    
                        case "alterarStatus":
                            idAnuncio = dados.get("idAnuncio")
                            statusAnuncio = Status[dados.get("statusAnuncio")]
                            for anuncio in self.loja.anuncios:
                                if idAnuncio == anuncio.idAnuncio:
                                    anuncio.alterarStatus(statusAnuncio)
                            self.visibilidade_anuncio_alterada.emit(statusAnuncio.name)

                        case "alterarProduto":
                            idAnuncio = dados.get("idAnuncio")
                            idProduto = dados.get("idProduto")
                            for anuncio in self.loja.anuncios:
                                if idAnuncio == anuncio.idAnuncio:
                                    anuncio.alterarIdProduto(idProduto)
                            

                        case "alterarNomeProduto":
                            idProduto = dados.get("idProduto")
                            nome = dados.get("nome")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarNome(nome)
                            self.nome_produto_alterado.emit(nome)
                                    
                        case "alterarDescricaoProduto":
                            idProduto = dados.get("idProduto")
                            descricaoProduto = dados.get("descricao")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarDescricao(descricaoProduto)
                            self.descricao_produto_alterada.emit(descricaoProduto)
                                    
                        case "alterarPreco":
                            idProduto = dados.get("idProduto")
                            preco = dados.get("preco")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarPreco(preco)
                            self.preco_produto_alterado.emit(preco)
                                    
                        case "alterarEstoque":
                            idProduto = dados.get("idProduto")
                            estoque = dados.get("estoque")
                            for produtos in self.loja.produtos:
                                if idProduto == produtos.idProduto:
                                    produtos.alterarEstoque(estoque)
                            self.estoque_produto_alterado.emit(estoque)
                                    
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
                            if dados.get("status") == "ok":
                                qntAnuncios = dados.get("qntAnuncio", 0)
                                idsAnuncio = dados.get("idsAnuncio", [])
                                categorias = dados.get("categorias", [])
                                statusAnuncio = dados.get("statusAnuncio", [])
                                idsProduto = dados.get("idsProduto", [])
                                idsLoja = dados.get("idsLoja", [])
                                
                                self.anuncios.clear()
                                for i in range (qntAnuncios):
                                    anuncio = Anuncio(idsProduto[i], categorias[i], Status[statusAnuncio[i]], idsAnuncio[i], idsLoja[i])
                                    self.anuncios.append(anuncio)
                                self.anuncios_recuperados.emit(self.anuncios)
                            else:
                                print("Erro ao recuperar anúncios:", dados.get("resposta"))
                        
                        case "recuperaProdutos":
                            if dados.get("status") == "ok":
                                qntProdutos = dados.get("qntProduto")
                                idsProdutos = dados.get("idsProduto")
                                nomes = dados.get("nomes")
                                descricoes = dados.get("descricoes")
                                precos = dados.get("precos")
                                estoques = dados.get("estoques")
                                idsLoja = dados.get("idsLoja")
                                
                                self.produtos.clear()
                                for i in range (qntProdutos):
                                    produto = Produto(idsProdutos[i], nomes[i], descricoes[i], precos[i], estoques[i], idsLoja[i])
                                    self.produtos.append(produto)
                                self.produtos_recuperados.emit(self.produtos)
                        
                        case "recuperaLoja":
                            if dados.get("status") == "ok":
                                idLoja = dados.get("idLoja")
                                idUsuario = dados.get("idUsuario")
                                nomeLoja = dados.get("nome")
                                endereco = dados.get("endereco")
                                descricaoLoja = dados.get("descricao")
                                self.loja = Loja(idLoja, idUsuario, nomeLoja, endereco, descricaoLoja)
                                self.loja_recuperada.emit(nomeLoja, descricaoLoja, endereco)
            
                        case "recuperaCarrinho":
                            if dados.get("status") == "ok":
                                idCarrinho = dados.get("idCarrinho")
                                total = dados.get("total")
                                
                                carrinho = Carrinho(idCarrinho)
                                carrinho.total = total
                                self.carrinho = carrinho
                        
                        case "recuperaItens":
                            status = dados.get("status")
                            if status == "ok":
                                qntItem = dados.get("qntItem")
                                idsItem = dados.get("idsItem")
                                idsProduto = dados.get("idsProduto")
                                quantidades = dados.get("quantidades")
                                
                                for i in range(qntItem):
                                    for produto in self.produtos:
                                        if produto.idProduto == idsProduto[i]:
                                            preco = produto.preco
                                    item = Item(idsProduto[i], preco, idsItem[i], quantidades[i])
                                    self.carrinho.itens.append(item)
                        
                        case "recuperaAnunciosUser":
                            status = dados.get("status")
                            if status == "ok":
                                qntAnuncio = dados.get("qntAnuncio")
                                idsAnuncio = dados.get("idsAnuncio")
                                categorias = dados.get("categorias")
                                statusAnuncio = dados.get("statusAnuncio")
                                idsProduto = dados.get("idsProduto")
                                idLoja = dados.get("idLoja")
                                
                                print(f"ID Loja: {idLoja}")
                                print(f"Qnt Anuncio: {qntAnuncio}")
                                print(f"IDs Anuncio: {idsAnuncio}")
                                print(f"Categorias: {categorias}")
                                print(f"Status Anuncio: {statusAnuncio}")
                                print(f"IDs Produto: {idsProduto}")
                                self.loja.anuncios.clear()
                                for i in range (qntAnuncio):
                                    anuncio = Anuncio(idsProduto[i], categorias[i], Status[statusAnuncio[i]], idsAnuncio[i], idLoja)
                                    self.loja.anuncios.append(anuncio)
                                
                                self.anuncios_user_recuperados.emit(self.loja.anuncios)
                        
                        case "recuperaProdutosUser":
                            status = dados.get("status")
                            if status == "ok":
                                qntProdutos = dados.get("qntProduto")
                                idsProdutos = dados.get("idsProduto")
                                nomes = dados.get("nomes")
                                descricoes = dados.get("descricoes")
                                precos = dados.get("precos")
                                estoques = dados.get("estoques")
                                idLoja = dados.get("idLoja")

                                print(f"Qnt Produtos: {qntProdutos}")
                                print(f"IDs Produtos: {idsProdutos}")
                                print(f"Nomes: {nomes}")
                                print(f"Descrições: {descricoes}")
                                print(f"Preços: {precos}")
                                print(f"Estoques: {estoques}")
                                print(f"ID Loja: {idLoja}")

                                self.loja.produtos.clear()
                                for i in range (qntProdutos):
                                    produto = Produto(idsProdutos[i], nomes[i], descricoes[i], precos[i], estoques[i], idLoja)
                                    self.loja.produtos.append(produto)
                                self.produtos_user_recuperados.emit(self.loja.produtos)

                        case _:
                            print("Comando desconhecido recebido do servidor.")
                    
            except Exception as e:
                print(f"Erro ao escutar o servidor: {e}")
                continue

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
            
        except Exception as e:
            print(f"\n Erro: {e}")
            
    def criarAnuncio(self, categoria:Categoria, status:Status, idProduto:int):
        try:
            payload = {
                "comando": "criarAnuncio",
                "parametros": {
                    "categoria": categoria,
                    "statusAnuncio": status.name,
                    "idLoja":self.loja.idLoja,
                    "idProduto": idProduto
                }
            }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       

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

        except Exception as e:
            print(f"\n Erro: {e}")
        
    def fazerLogin(self, email: str, senha:str):
        try:
            payload = {
                "comando": "fazerLogin",
                "parametros":{
                    "email":email,
                    "senha": senha
                }
            }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       
            
        except Exception as e:
            print(f"\n Erro: {e}")
            
    
    def recuperaLoja(self, idLoja: int, idUsuario):
        try:
            payload = {
                "comando": "recuperaLoja",
                "parametros": {
                    "idLoja": idLoja,
                    "idUsuario": idUsuario
                }
            }
            print("Recuperando loja 2")
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()
            print("Recuperando loja 3")
            
        except Exception as e:
            print(f"Erro: {e}")
    
    
    def recuperaProdutosUser(self, idLoja: int):
        print("Recuperando produtos da loja 2")
        try:
            payload = {
                "comando": "recuperaProdutosUser",
                "parametros": {
                    "idLoja": idLoja
                }
            }
            print(f"{payload}")
            self.sockFile.write(json.dumps(payload) + "\n")
            print("Recuperando produtos da loja 3")
            self.sockFile.flush()
            
        except Exception as e:
            print(f"Erro: {e}")

    
    def recuperaAnunciosUser(self, idLoja: int):
        try:
            payload = {
                "comando": "recuperaAnunciosUser",
                "parametros": {
                    "idLoja": idLoja
                }
            }
            self.sockFile.write(json.dumps(payload) + "\n")
            self.sockFile.flush()
            
        except Exception as e:
            print(f"Erro: {e}")
    
    def recuperaCarrinho(self, idUsuario: int):
        try:
            payload = {
                "comando": "recuperaCarrinho",
                "parametros": {
                    "idUsuario": idUsuario
                }
            }
            self.sockFile.write(json.dumps(payload) + "\n")
            self.sockFile.flush()
            
        except Exception as e:
            print(f"Erro: {e}")
        
    def recuperaItens(self, idCarrinho: int):
        try:
            payload = {
                "comando": "recuperaItens",
                "parametros": {
                    "idCarrinho": idCarrinho
                }
            }
            self.sockFile.write(json.dumps(payload) + "\n")
            self.sockFile.flush()
            
        except Exception as e:
            print(f"Erro: {e}")
    
    def excluirLoja(self, idLoja:int):
            print(f"Excluindo loja: {idLoja}")
            try:
                payload = {
                    "comando": "excluirLoja",
                    "parametros" :{
                        "idLoja": idLoja
                    }
                }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()      

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

            except Exception as e:
                print(f"\n Erro: {e}")

    def alterarEndereco(self,endereco:str):
            try:
                payload = {
                    "comando": "alterarEndereco",
                    "parametros" :{
                        "endereco": endereco    
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       

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

            except Exception as e:
                print(f"\n Erro: {e}")

    def alterarCategoria(self,idAnuncio:int, categoria: Categoria):
            try:
                payload = {
                    "comando": "alterarCategoria",
                    "parametros" :{
                        "idAnuncio": idAnuncio,
                        "categoria": categoria.name   
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       

            except Exception as e:
                print(f"\n Erro: {e}")
   
    def alterarStatus(self,idAnuncio:int, status:Status):
            try:
                payload = {
                    "comando": "alterarStatus",
                    "parametros" :{
                        "idAnuncio": idAnuncio,
                        "statusAnuncio": status.name  
                    }  
            }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       

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

            except Exception as e:
                print(f"\n Erro: {e}")        
    
    def fecharCarrinho(self, idCarrinho):
            try:
                payload = {
                    "comando": "fecharCarrinho",
                    "parametros": {
                        "idCarrinho": idCarrinho
                    }
                }
                self.sockFile.write(json.dumps(payload) + '\n')
                self.sockFile.flush()       

            except Exception as e:
                print(f"\n Erro: {e}")       
                      
    def recuperaAnuncios (self):
        try:
            payload = {
                "comando": "recuperaAnuncios"
            }
            self.sockFile.write(json.dumps(payload) + '\n')
            self.sockFile.flush()       

        except Exception as e:
            print(f"\n Erro: {e}")
            
    
    def recuperaProdutos(self):
        try:
            payload = {
                "comando": "recuperaProdutos"
            }
            self.sockFile.write(json.dumps(payload) + "\n")
            self.sockFile.flush()
            
        except Exception as e:
            print(f"Erro: {e}")

