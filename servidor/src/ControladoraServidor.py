from Loja import Loja
from Anuncio import Anuncio
from Produto import Produto
from Categoria import Categoria
from Status import Status
from AcessoBanco import AcessoBanco
import json

# Iniciara o processamento da tarefa requerida pelo cliente
# Para decidir a operação, poderiamos ter um campo no JSON com essa informação
class ControladoraServidor:
    
    
    def __init__(self, socketCliente, addr):
        self.socketCliente = socketCliente
        self.addr = addr
        self.fileCliente = socketCliente.makefile(mode='rw')
        self.loja = None
        
    # vai controlar a execução
    def executa(self):
        self.banco = AcessoBanco()
        print(f"Cliente conectado: {self.addr}")
        try:
            while True:
                linha = self.fileCliente.readline()
                if not linha:
                    break # encerra a conexão
                try:
                    payload = json.loads(linha)
                    resposta = self.comandos(payload)
                    self.fileCliente.write(json.dumps(resposta) + '\n')
                    self.fileCliente.flush()
                except json.JSONDecodeError:
                    self.fileCliente.write(json.dumps({"status": "erro", "resposta": "JSON inválido"}) + '\n')
                    self.fileCliente.flush()
        except Exception as e:
            print(f"Erro com {self.addr}: {e}")
        finally:                
            print(f"Cliente {self.addr} desconectado")
            self.socketCliente.close()
                    
    
    # identifica e executa o comando passado (adicionar mais comandos)
    def comandos(self, payload):
        cmd = payload.get("comando")
        parametros = payload.get("parametros", {})
        
        print(f"[{self.addr}] -> Comando: {cmd} | Parametros: {parametros}")
        
        if cmd == "criarLoja":
            nomeLoja = parametros.get("nome")
            descricaoLoja = parametros.get("descricao")
            endereco = parametros.get("endereco")
            idUsuario = parametros.get("idUsuario")
            if nomeLoja and descricaoLoja and endereco and idUsuario:
                self.criarLoja(nomeLoja, endereco, descricaoLoja, idUsuario)
                return {
                    "status": "ok",
                    "resposta": "Loja criada com sucesso"
                }
            else:
                return {
                    "status": "erro",
                    "resposta": "Parâmetros inválidos"
                }
        else:
            return {"status": "erro", "resposta": "Comando desconhecido"}
    
    
    # Cria uma Loja e adiciona ela no banco
    def criarLoja(self, nome: str, endereco: str, descricao: str, idUsuario: int):
        loja = Loja(nome, endereco, descricao, idUsuario)
        self.loja = loja
        loja.criarLojaBanco(self.banco)
        print("Loja Adicionada no Banco!\n")
        return loja.idLoja
    
    # Cria um Anuncio e adiciona ele no banco
    def criarAnuncio(self, categoria: Categoria, status: Status, idLoja: int, idProduto: int):
        anuncio = Anuncio(idProduto, idLoja, categoria, status)
        anuncio.criarAnuncioBanco(self.banco)
        self.loja.adicionaAnuncio(anuncio)
        return anuncio.idAnuncio
    
    # Cria um Produto e adiciona ele no banco
    def criarProduto(self, nome: str, descricao: str, preco: float, estoque: int):
        produto = Produto(nome, descricao, preco, estoque)
        produto.criarProdutoBanco(self.banco)
        return produto.idProduto

    # Adiciona as informações do usuario no banco
    def cadastrarUsuario(self, idUser: int, nome: str, email: str, senha: str):
        self.banco.cadastrarUsuario(idUser, nome, email, senha)
    
    
    # verifica se as informações passadas são iguais as do banco
    def fazerLogin(self, idUser: int, email: str, senha: str):
        emailBanco, senhaBanco = self.banco.recuperaLogin(idUser)
        
        if (emailBanco == email and senhaBanco == senha):
            return 200
        else:
            return 403