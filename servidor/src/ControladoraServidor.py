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
        comando = payload.get("comando")
        parametros = payload.get("parametros", {})
        
        print(f"[{self.addr}] -> Comando: {comando} | Parametros: {parametros}")
        
        match comando:
            case "criarLoja":
                nomeLoja = parametros.get("nome")
                descricaoLoja = parametros.get("descricao")
                endereco = parametros.get("endereco")
                idUsuario = parametros.get("idUsuario")
                if nomeLoja and descricaoLoja and endereco and idUsuario:
                    response = self.criarLoja(nomeLoja, endereco, descricaoLoja, idUsuario)
                    return {
                        "comando": "criarLoja",
                        "status": "ok",
                        "resposta": "Loja criada com sucesso",
                        "idLoja": response
                    }
                else:
                    return {
                        "comando": "criarLoja",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }

            case "criarAnuncio":
                categoria = parametros.get("categoria")
                status = parametros.get("status")
                idLoja = self.loja.idLoja
                idProduto = parametros.get("idProduto")
                if categoria and status and idLoja and idProduto:
                    response = self.criarAnuncio(categoria, status, idLoja, idProduto)
                    return{
                        "comando": "criarAnuncio",
                        "status": "ok",
                        "resposta": "Anúncio criado com sucesso",
                        "idAnuncio": response
                    }
                else:
                    return{
                        "comando": "criarAnuncio",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                    
            case "criarProduto":
                nomeProduto = parametros.get("nome")
                descricao = parametros.get("descricao")
                preco = parametros.get("preco")
                estoque = parametros.get("estoque")
                idLoja = self.loja.idLoja
                if nomeProduto and descricao and preco and estoque and idLoja:
                    response = self.criarProduto(nomeProduto, descricao, preco, estoque, idLoja)
                    return{
                        "comando": "criarProduto",
                        "status": "ok",
                        "resposta": "Produto criado com sucesso",
                        "idProduto": response
                    }
                else:
                    return{
                        "comando": "criarProduto",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                    
            case "cadastrarUsuario":
                nomeUser = parametros.get("nome")
                email = parametros.get("email")
                senha = parametros.get("senha")
                if nomeUser and email and senha:
                    idUsuario, idCarrinho = self.cadastrarUsuario(nomeUser, email, senha)
                    return{
                        "comando": "cadastrarUsuario",
                        "status": "ok",
                        "resposta": "Usuário cadastrado com sucesso",
                        "idUsuario": idUsuario,
                        "idCarrinho": idCarrinho
                    }
                else:
                    return {
                        "comando": "cadastrarUsuario",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                    
            case "fazerLogin":
                idUsuario = parametros.get("idUser")
                email = parametros.get("email")
                senha = parametros.get("senha")
                if idUsuario and email and senha:
                    response = self.fazerLogin(idUsuario, email, senha)
                    if response == 200:
                        return{
                            "comando": "fazerLogin",
                            "status": "ok",
                            "resposta": "Usuário logado com sucesso"
                        }
                    else:
                        return {
                            "comando": "fazerLogin",
                            "status": "erro",
                            "resposta": "Usuário não cadastrado"
                        }
                else:
                    return {
                        "comando": "fazerLogin",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "excluirLoja":
                self.excluirLoja(self.banco)
                return{
                    "comando": "excluirLoja",
                    "status": "ok",
                    "resposta": "Loja excluída com sucesso"
                }
            
            case "excluirAnuncio":
                idAnuncio = parametros.get("idAnuncio")
                if idAnuncio:
                    self.excluirAnuncio(idAnuncio, self.banco)
                    return{
                        "comando": "excluirAnuncio",
                        "status": "erro",
                        "resposta": "Anuncio excluído com sucesso"
                    }
                else:
                    return{
                        "comando": "excluirAnuncio",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                
            case "excluirProduto":
                idProduto = parametros.get("idProduto")
                if idProduto:
                    self.excluirAnuncio(idProduto, self.banco)
                    return{
                        "comando": "excluirProduto",
                        "status": "erro",
                        "resposta": "Produto excluído com sucesso"
                    }
                else:
                    return{
                        "comando": "excluirProduto",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarNomeLoja":
                nomeLoja = parametros.get("nome")
                if nomeLoja:
                      self.alterarNomeLoja(nomeLoja)
                      return{
                          "comando": "alterarNomeLoja",
                          "status": "ok",
                          "resposta": "Nome da loja alterado com sucesso"
                      }
                else:
                    return{
                        "comando": "alterarNomeLoja",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                    
            case "alterarEndereco":
                endereco = parametros.get("endereco")
                if endereco:
                    self.alterarEndereco(endereco)
                    return{
                        "comando": "alterarEndereco",
                        "status": "ok",
                        "resposta": "Endereço da loja alterado com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarEndereco",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarDescricaoLoja":
                descricaoLoja = parametros.get("descricao")
                if descricaoLoja:
                    self.alterarDescricaoLoja(descricao)
                    return{
                        "comando": "alterarDescricaoLoja",
                        "status": "ok",
                        "resposta": "Descrição da Loja alterada com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarDescricaoLoja",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarCategoria":
                idAnuncio = parametros.get("idAnuncio")
                categoria = parametros.get("categoria")
                if idAnuncio and categoria:
                    self.alterarCategoria(idAnuncio, categoria)
                    return{
                        "comando": "alterarCategoria",
                        "status": "ok",
                        "resposta": "Categoria alterada com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarCategoria",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }  
            
            case "alterarStatus":
                idAnuncio = parametros.get("idAnuncio")
                status = parametros.get("status")
                if idAnuncio and status:
                    self.alterarStatus(idAnuncio, status)
                    return{
                        "comando": "alterarStatus",
                        "status": "ok",
                        "resposta": "Status alterado com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarStatus",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }  
            
            case "alterarProduto":
                idAnuncio = parametros.get("idAnuncio")
                idProduto = parametros.get("idProduto")
                if idAnuncio and idProduto:
                    self.alterarProduto(idAnuncio, idProduto)
                    return{
                        "comando": "alterarProduto",
                        "status": "ok",
                        "resposta": "Produto alterado com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarProduto",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarNomeProduto":
                idProduto = parametros.get("idProduto")
                nomeProduto = parametros.get("nome")
                if idProduto and nomeProduto:
                    self.alterarNomeProduto(idProduto, nomeProduto)
                    return{
                        "comando": "alterarNomeProduto",
                        "status": "ok",
                        "resposta": "O nome do produto foi alterado com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarNomeProduto",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarDescricaoProduto":
                idProduto = parametros.get("idProduto")
                descricaoProduto = parametros.get("descricao")
                if idProduto and descricaoProduto:
                    self.alterarDescricaoProduto(idProduto, descricaoProduto)
                    return{
                        "comando": "alterarDescricaoProduto",
                        "status": "ok",
                        "resposta": "Descrição do produto alterada com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarDescricaoProduto",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarPreco":
                idProduto = parametros.get("idProduto")
                preco = parametros.get("preco")
                if idProduto and preco:
                    self.alterarPreco(idProduto, preco)
                    return{
                        "comando": "alterarPreco",
                        "status": "ok",
                        "resposta": "Preco do produto alterado com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarPreco",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarEstoque":
                idProduto = parametros.get("idProduto")
                estoque = parametros.get("estoque")
                if idProduto and estoque:
                    self.alterarEstoque(idProduto, estoque)
                    return{
                        "comando": "alterarEstoque",
                        "status": "ok",
                        "resposta": "Estoque alterado com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarEstoque",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "adicionarItem":
                idCarrinho = parametros.get("idCarrinho")
                idProduto = parametros.get("idProduto")
                quantidade = parametros.get("quantidade")
                if idCarrinho and idProduto and quantidade:
                    idItem, preco = self.adicionarItem(idCarrinho, idProduto, quantidade)
                    return {
                        "comando": "adicionarItem",
                        "status": "ok",
                        "resposta": "Item adicionado com sucesso",
                        "idItem": idItem,
                        "preco": preco
                    }
                else:
                    return{
                        "comando": "adicionarItem",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarQuantidade":
                idItem = parametros.get("idItem")
                quantidade = parametros.get("quantidade")
                if idItem and quantidade:
                    self.alterarQuantidade(idItem, quantidade)
                    return{
                        "comando": "alterarQuantidade",
                        "status": "ok",
                        "resposta": "Quantidade alterada com sucesso"
                    }
                else:
                    return{
                        "comando": "alterarQuantidade",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "fecharCarrinho":
                idCarrinho = parametros.get("idCarrinho")
                if idCarrinho:
                    codigo = self.fecharCarrinho(idCarrinho)
                    if codigo == 200:
                        return {
                            "comando": "fecharCarrinho",
                            "status": "ok",
                            "resposta": "Carrinho fechado com sucesso",
                            "codigo": codigo
                        }
                    else:
                        return {
                            "comando": "fecharCarrinho",
                            "status": "erro",
                            "resposta": "Estoque insuficiente",
                            "codigo": codigo
                        }
                else:
                    return{
                        "comando": "fecharCarrinho",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "recuperaAnuncios":
                anuncios = self.recuperaAnuncios()
                if anuncios:
                    return {
                        "comando": "recuperaAnuncios",
                        "status": "ok",
                        "resposta": "Todos os anuncios foram recuperados",
                        "anuncios": anuncios
                    }
                else:
                    return {
                        "comando": "recuperaAnuncios",
                        "status": "erro",
                        "resposta": "Erro ao recuperar os anuncios do banco"
                    }
            
            case _:
                return {"status": "erro", "resposta": "Comando desconhecido"}
    
    
    # Operações de Criação:
    def criarLoja(self, nome: str, endereco: str, descricao: str, idUsuario: int):
        loja = Loja(nome, endereco, descricao, idUsuario)
        self.loja = loja
        loja.criarLojaBanco(self.banco)
        return loja.idLoja
    
    def criarAnuncio(self, categoria: Categoria, status: Status, idLoja: int, idProduto: int):
        anuncio = Anuncio(idProduto, idLoja, categoria, status)
        anuncio.criarAnuncioBanco(self.banco)
        self.loja.adicionaAnuncio(anuncio)
        return anuncio.idAnuncio
    
    def criarProduto(self, nome: str, descricao: str, preco: float, estoque: int, idLoja: int):
        produto = Produto(nome, descricao, preco, estoque, idLoja)
        self.produtos.append(produto)
        self.loja.adicionaProduto(produto)
        produto.criarProdutoBanco(self.banco)
        return produto.idProduto

    # Operações de Login e Cadastro
    def cadastrarUsuario(self, nome: str, email: str, senha: str):
        idCarrinho = self.banco.criarCarrinho()
        idUsuario = self.banco.cadastrarUsuario(nome, email, senha, idCarrinho)
        return idUsuario, idCarrinho
    
    def fazerLogin(self, idUser: int, email: str, senha: str):
        emailBanco, senhaBanco = self.banco.recuperaLogin(idUser)
        
        if (emailBanco == email and senhaBanco == senha):
            return 200
        else:
            return 403
    
    
    # Operações de Edição da Loja:
    def alterarNomeLoja(self, nome: str):
        self.loja.nome = nome
        self.loja.alterarNomeLoja(nome, self.banco)
    
    def alterarEndereco(self, endereco: str):
        self.loja.endereco = endereco
        self.loja.alterarEndereco(endereco, self.banco)
    
    def alterarDescricaoLoja(self, descricao: str):
        self.loja.descricao = descricao
        self.loja.alterarDescricaoLoja(descricao, self.banco)
    
    
    # Operações de Edição do Anuncio
    def alterarCategoria(self, idAnuncio: int, categoria: Categoria):
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.categoria = categoria
                anuncio.alterarCategoria(categoria, self.banco)
        
    def alterarStatus(self, idAnuncio: int, status: Status):
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.status = status
                anuncio.alterarStatus(status, self.banco)
    
    def alterarProduto(self, idAnuncio: int, idProduto: int):
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.idProduto = idProduto
                anuncio.alterarProduto(idProduto, self.banco)


    # Operações de Edição do Produto
    def alterarNomeProduto(self, idProduto: int, nome: str):
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.nome = nome
                produto.alterarProduto(nome, self.banco)
            
    def alterarDescricaoProduto(self, idProduto: int, descricao: str):
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.descricao = descricao
                produto.alterarProduto(descricao, self.banco)
                
    def alterarPreco(self, idProduto: int, preco: float):
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.preco = preco
                produto.alterarProduto(preco, self.banco)
                
    def alterarEstoque(self, idProduto: int, estoque: int):
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.estoque = estoque
                produto.alterarProduto(estoque, self.banco)
    
    
    # Operações de Exclusão:
    def excluirLoja(self, banco: AcessoBanco):
        self.loja.excluirLoja(banco)
        self.loja = None
    
    def excluirAnuncio(self, idAnuncio: int, banco: AcessoBanco):
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.excluirAnuncio(banco)
                self.loja.anuncios.remove(anuncio)
                break
    
    def excluirProduto(self, idProduto: int, banco: AcessoBanco):
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.excluirProduto(banco)
                for anuncio in self.loja.anuncios:
                    if anuncio.idProduto == idProduto:
                        self.excluirAnuncio(anuncio.idAnuncio, banco)
                self.loja.produtos.remove(produto)
                break
    
    
    # Funções de edição do carrinho
    def adicionarItem(self, idCarrinho: int, idProduto: int, quantidade: int):
        idItem = self.banco.adicionarItem(idCarrinho, idProduto, quantidade)
        self.banco.cur.execute("SELECT preco FROM produto WHERE idProduto = ?", (idProduto,))
        result = self.banco.cur.fetchone()
        preco = result[0]
        self.banco.con.commit()
        
        return idItem, preco
    
    def alterarQuantidade(self, idItem: int, quantidade: int):
        self.banco.alterarQuantidade(idItem, quantidade)
    
    def fecharCarrinho(self, idCarrinho: int):
        self.banco.cur.execute("SELECT idItem, FK_produto, quantidade FROM item WHERE FK_idCarrinho = ?", (idCarrinho,))
        itens = self.banco.cur.fetchall()

        for item in itens:
            idItem, idProduto, quantidade = item
            self.banco.cur.execute("SELECT estoque FROM produto WHERE idProduto = ?", (idProduto,))
            estoque = self.banco.cur.fetchone()[0]

            if quantidade > estoque:
                return 403

        for item in itens:
            idItem, idProduto, quantidade = item
            self.banco.cur.execute("SELECT estoque FROM produto WHERE idProduto = ?", (idProduto,))
            estoque = self.banco.cur.fetchone()[0]
            novoEstoque = estoque - quantidade

            self.alterarEstoque(idProduto, novoEstoque)
            self.banco.cur.execute("DELETE FROM item WHERE idItem = ?", (idItem,))

        self.banco.con.commit()
        return 200
        
    
    # Função responsável por iniciar o feed com os Anuncios
    def recuperaAnuncios(self):
        self.banco.cur.execute("SELECT * FROM anuncio")
        anunciosBanco = self.banco.cur.fetchall()
        anuncios = []
        
        for anuncio in anunciosBanco:
            idAnuncio, categoria, statusAnuncio, idProduto, idLoja = anuncio
            anuncioAux = Anuncio(idProduto, idLoja, categoria, statusAnuncio)
            anuncioAux.idAnuncio = idAnuncio
            anuncios.append(anuncioAux)
        
        return anuncios