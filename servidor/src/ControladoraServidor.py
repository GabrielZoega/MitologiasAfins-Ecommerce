from Loja import Loja
from Anuncio import Anuncio
from Produto import Produto
from Categoria import Categoria
from Status import Status
from AcessoBanco import AcessoBanco
import json

# Iniciara o processamento da tarefa requerida pelo cliente
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
                    print(f"\n\nPayload recebido: {payload}\n\n")
                    resposta = self.comandos(payload)
                    self.fileCliente.write(json.dumps(resposta) + '\n')
                    self.fileCliente.flush()
                except json.JSONDecodeError:
                    self.fileCliente.write(json.dumps({"status": "erro", "resposta": "JSON inválido"}) + '\n')
                    self.fileCliente.flush()
        #except Exception as e:
        #    print(f"Erro com {self.addr}: {e}")
        finally:                
            print(f"Cliente {self.addr} desconectado")
            self.socketCliente.close()
                    
    
    # identifica e executa o comando enviado pelo cliente
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
                statusAnuncio = parametros.get("statusAnuncio")
                idLoja = self.loja.idLoja
                idProduto = parametros.get("idProduto")
                if categoria and statusAnuncio and idLoja and idProduto:
                    response = self.criarAnuncio(categoria, statusAnuncio, idLoja, idProduto)
                    return{
                        "comando": "criarAnuncio",
                        "status": "ok",
                        "resposta": "Anúncio criado com sucesso",
                        "idAnuncio": response,
                        "idLoja": idLoja,
                        "idProduto": idProduto,
                        "categoria": categoria,
                        "statusAnuncio": statusAnuncio
                    }
                else:
                    return{
                        "comando": "criarAnuncio",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                    
            case "criarProduto":
                nomeProduto = parametros.get("nomeProduto")
                descricao = parametros.get("descricao")
                preco = parametros.get("preco")
                estoque = parametros.get("estoque")
                idLoja = parametros.get("idLoja")
                if nomeProduto is not None and descricao is not None and preco is not None and estoque is not None and idLoja is not None:
                    response = self.criarProduto(nomeProduto, descricao, preco, estoque, idLoja)
                    return{
                        "comando": "criarProduto",
                        "status": "ok",
                        "resposta": "Produto criado com sucesso",
                        "idProduto": response,
                        "idLoja": idLoja
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
                print(f"Nome: {nomeUser}, Email: {email}, Senha: {senha}")
                if nomeUser and email and senha:
                    idUsuario, idCarrinho = self.cadastrarUsuario(nomeUser, email, senha)
                    return{
                        "comando": "cadastrarUsuario",
                        "status": "ok",
                        "resposta": "Usuário cadastrado com sucesso",
                        "idUsuario": idUsuario,
                        "idCarrinho": idCarrinho,
                        "nome": nomeUser,
                        "email": email,
                        "senha": senha
                    }
                else:
                    return {
                        "comando": "cadastrarUsuario",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                    
            case "fazerLogin":
                email = parametros.get("email")
                senha = parametros.get("senha")
                if email and senha:
                    resultado = self.fazerLogin(email)
                    if resultado[0] is None:
                        return {
                            "comando": "fazerLogin",
                            "status": "erro",
                            "resposta": "Usuário não cadastrado"
                        }
                    idUsuario, nome, emailBanco, senhaBanco, tipoUsuario, idLoja, idCarrinho = resultado
                    if email == emailBanco and senha == senhaBanco:
                        return{
                            "comando": "fazerLogin",
                            "status": "ok",
                            "resposta": "Usuário logado com sucesso",
                            "idUsuario": idUsuario,
                            "nome": nome,
                            "email": emailBanco,
                            "senha": senhaBanco,
                            "tipoCliente": tipoUsuario,
                            "idLoja": idLoja,
                            "idCarrinho": idCarrinho
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
                    
            case "recuperaLoja":
                idLoja = parametros.get("idLoja")
                idUsuario = parametros.get("idUsuario")
                nomeLoja, endereco, descricaoLoja = self.recuperaLoja(idLoja, idUsuario)
                if nomeLoja and endereco and descricaoLoja:
                    return{
                        "comando": "recuperaLoja",
                        "status": "ok",
                        "resposta": "Loja recuperada com sucesso",
                        "idUsuario": idUsuario,
                        "idLoja": idLoja,
                        "nome": nomeLoja,
                        "endereco": endereco,
                        "descricao": descricaoLoja
                    }
                else:
                    return {
                        "comando": "recuperaLoja",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
                
            case "recuperaProdutosUser":
                idLoja = parametros.get("idLoja")
                qntProdutos, idsProduto, nomesProduto, descricoesProduto, precos, estoques, idLoja = self.recuperaProdutosUser(idLoja)
                if qntProdutos is not None and idsProduto is not None and nomesProduto is not None and descricoesProduto is not None and precos is not None and estoques is not None and idLoja is not None:
                    return {
                        "comando": "recuperaProdutosUser",
                        "status": "ok",
                        "resposta": "Produtos recuperados com sucesso",
                        "qntProduto": qntProdutos,
                        "idsProduto": idsProduto,
                        "nomes": nomesProduto,
                        "descricoes": descricoesProduto,
                        "precos": precos,
                        "estoques": estoques,
                        "idLoja": idLoja
                    }
                else:
                    return {
                        "comando": "recuperaProdutosUser",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "recuperaAnunciosUser":
                idLoja = parametros.get("idLoja")
                qntAnuncios, idsAnuncio, categorias, statusAnuncio, idsProduto = self.recuperaAnunciosUser(idLoja)
                print(f"idsproduto: {idsProduto}")
                if qntAnuncios and idsAnuncio and categorias and statusAnuncio and idsProduto:
                    return {
                        "comando": "recuperaAnunciosUser",
                        "status": "ok",
                        "resposta": "Todos os anuncios do usuário foram recuperados",
                        "qntAnuncio": qntAnuncios,
                        "idsAnuncio": idsAnuncio,
                        "categorias": categorias,
                        "statusAnuncio": statusAnuncio,
                        "idsProduto": idsProduto,
                        "idLoja": idLoja
                    }
                else:
                    return {
                        "comando": "recuperaAnunciosUser",
                        "status": "erro",
                        "resposta": "Erro ao recuperar os anuncios do banco"
                    }
                
            case "excluirLoja":
                idLoja = parametros.get("idLoja")
                self.excluirLoja(self.banco, idLoja)
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
                        "status": "ok",
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
                        "status": "ok",
                        "resposta": "Produto excluído com sucesso"
                    }
                else:
                    return{
                        "comando": "excluirProduto",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarNomeLoja":
                nomeLoja = parametros.get("nomeLoja")
                if nomeLoja:
                      self.alterarNomeLoja(nomeLoja)
                      return{
                          "comando": "alterarNomeLoja",
                          "status": "ok",
                          "resposta": "Nome da loja alterado com sucesso",
                          "nomeLoja": nomeLoja
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
                        "resposta": "Endereço da loja alterado com sucesso",
                        "endereco": endereco
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
                    self.alterarDescricaoLoja(descricaoLoja)
                    return{
                        "comando": "alterarDescricaoLoja",
                        "status": "ok",
                        "resposta": "Descrição da Loja alterada com sucesso",
                        "descricao": descricaoLoja
                    }
                else:
                    return{
                        "comando": "alterarDescricaoLoja",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }
            
            case "alterarCategoria":
                idAnuncio = parametros.get("idAnuncio")
                categoria = Categoria[parametros.get("categoria")]
                if idAnuncio and categoria:
                    self.alterarCategoria(idAnuncio, categoria)
                    return{
                        "comando": "alterarCategoria",
                        "status": "ok",
                        "resposta": "Categoria alterada com sucesso",
                        "categoria": categoria.value
                    }
                else:
                    return{
                        "comando": "alterarCategoria",
                        "status": "erro",
                        "resposta": "Parâmetros inválidos"
                    }  
            
            case "alterarStatus":
                idAnuncio = parametros.get("idAnuncio")
                statusAnuncio = Status[parametros.get("statusAnuncio")]
                if idAnuncio and statusAnuncio:
                    self.alterarStatus(idAnuncio, statusAnuncio)
                    return{
                        "comando": "alterarStatus",
                        "status": "ok",
                        "resposta": "Status alterado com sucesso",
                        "statusAnuncio": statusAnuncio.name
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
                        "resposta": "O nome do produto foi alterado com sucesso",
                        "nome": nomeProduto
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
                        "resposta": "Descrição do produto alterada com sucesso",
                        "descricao": descricaoProduto
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
                        "resposta": "Preco do produto alterado com sucesso",
                        "preco": preco
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
                        "resposta": "Estoque alterado com sucesso",
                        "estoque": estoque
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
                qntAnuncios, idsAnuncio, categorias, statusAnuncio, idsProduto, idsLoja = self.recuperaAnuncios()
                if qntAnuncios is not None and idsAnuncio is not None and categorias is not None and statusAnuncio is not None and idsProduto is not None and idsLoja is not None:
                    return {
                        "comando": "recuperaAnuncios",
                        "status": "ok",
                        "resposta": "Todos os anuncios foram recuperados",
                        "qntAnuncio": qntAnuncios,
                        "idsAnuncio": idsAnuncio,
                        "categorias": categorias,
                        "statusAnuncio": statusAnuncio,
                        "idsProduto": idsProduto,
                        "idsLoja": idsLoja 
                    }
                else:
                    return {
                        "comando": "recuperaAnuncios",
                        "status": "erro",
                        "resposta": "Erro ao recuperar os anuncios do banco"
                    }
            
            case "recuperaProdutos":
                qntProdutos, idsProduto, nomes, descricoes, precos, estoques, idsLoja = self.recuperaProdutos()
                if qntProdutos is not None and idsProduto is not None and nomes is not None and descricoes is not None and precos is not None and estoques is not None and idsLoja is not None:
                    return {
                        "comando": "recuperaProdutos",
                        "status": "ok",
                        "resposta": "Todos os produtos foram recuperados",
                        "qntProduto": qntProdutos,
                        "idsProduto": idsProduto,
                        "nomes": nomes,
                        "descricoes": descricoes,
                        "precos": precos,
                        "estoques": estoques,
                        "idsLoja": idsLoja
                    }
                else:
                    return {
                        "comando": "recuperaProdutos",
                        "status": "erro",
                        "resposta": "Erro ao recuperar os Produtos do banco"
                    }
            
            case "recuperaCarrinho":
                idUsuario = parametros.get("idUsuario")
                idCarrinho, total = self.recuperaCarrinho(idUsuario)            
                if idCarrinho is not None:
                    return{
                        "comando": "recuperaCarrinho",
                        "status": "ok",
                        "resposta": "Carrinho recuperado com sucesso",
                        "idCarrinho": idCarrinho,
                        "total": total
                    }
                else:
                    return {
                        "comando": "recuperaCarrinho",
                        "status": "erro",
                        "resposta": "Erro ao recuperar o Carrinho do banco"
                    }
            
            case "recuperaItens":
                idCarrinho = parametros.get("idCarrinho")
                qntItem, idsItem, idsProduto, quantidades = self.recuperaItens(idCarrinho)
                return {
                    "comando": "recuperaItens",
                    "status": "ok",
                    "resposta": "Itens recuperados com sucesso",
                    "qntItem": qntItem,
                    "idsItem": idsItem,
                    "idsProduto": idsProduto,
                    "quantidades": quantidades
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
        self.loja.adicionaProduto(produto)
        produto.criarProdutoBanco(self.banco)
        return produto.idProduto

    def cadastrarUsuario(self, nome: str, email: str, senha: str):
        idCarrinho = self.banco.criarCarrinho()
        idUsuario = self.banco.cadastrarUsuario(nome, email, senha, idCarrinho)
        return idUsuario, idCarrinho
    
    def fazerLogin(self, email):
        resultado = self.banco.recuperaLogin(email)
        if resultado is None:
            return None, None, None, None, None, None, None
        idUsuario, nome, emailBanco, senhaBanco, tipoUsuario, idLoja, idCarrinho = resultado
        return idUsuario, nome, emailBanco, senhaBanco, tipoUsuario, idLoja, idCarrinho
    
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
        print(f"Categoria: {categoria}")
        self.banco.cur.execute("UPDATE anuncio SET categoria = ? WHERE idAnuncio = ?", (categoria.name, idAnuncio))
        self.banco.con.commit()
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.categoria = categoria
                anuncio.alterarCategoria(categoria, self.banco)
        
    def alterarStatus(self, idAnuncio: int, status: Status):
        print(f"Status: {status}")
        self.banco.cur.execute("UPDATE anuncio SET statusAnuncio = ? WHERE idAnuncio = ?", (status.name, idAnuncio))
        self.banco.con.commit()
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.status = status
                anuncio.alterarStatus(status, self.banco)
    
    def alterarProduto(self, idAnuncio: int, idProduto: int):
        self.banco.cur.execute("UPDATE anuncio SET FK_idProduto = ? WHERE idAnuncio = ?", (idProduto, idAnuncio))
        self.banco.con.commit()
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.idProduto = idProduto
                anuncio.alterarProduto(idProduto, self.banco)


    def alterarNomeProduto(self, idProduto: int, nome: str):
        print(f"Nome: {nome}")
        self.banco.cur.execute("UPDATE produto SET nomeProduto = ? WHERE idProduto = ?", (nome, idProduto))
        self.banco.con.commit()
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.nome = nome
                produto.alterarProduto(nome, self.banco)
            
    def alterarDescricaoProduto(self, idProduto: int, descricao: str):
        print(f"Descricao: {descricao}")
        self.banco.cur.execute("UPDATE produto SET descricaoProduto = ? WHERE idProduto = ?", (descricao, idProduto))
        self.banco.con.commit()
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.descricao = descricao
                produto.alterarProduto(descricao, self.banco)
                
    def alterarPreco(self, idProduto: int, preco: float):
        print(f"Preco: {preco}")
        self.banco.cur.execute("UPDATE produto SET preco = ? WHERE idProduto = ?", (preco, idProduto))
        self.banco.con.commit()
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.preco = preco
                produto.alterarProduto(preco, self.banco)
                
    def alterarEstoque(self, idProduto: int, estoque: int):
        print(f"Estoque: {estoque}")
        self.banco.cur.execute("UPDATE produto SET estoque = ? WHERE idProduto = ?", (estoque, idProduto))
        self.banco.con.commit()
        for produto in self.loja.produtos:
            if produto.idProduto == idProduto:
                produto.estoque = estoque
                produto.alterarProduto(estoque, self.banco)


    # Operações de Exclusão:
    def excluirLoja(self, banco: AcessoBanco, idLoja: int):
        print(f"Excluindo loja: {idLoja}")
        self.banco.cur.execute("SELECT idProduto FROM produto WHERE FK_Loja = ?", (idLoja,))
        produtos = self.banco.cur.fetchall()
        for produto in produtos:
            idProduto = produto[0]
            self.excluirProduto(idProduto, banco)
        
        self.banco.cur.execute("SELECT idAnuncio FROM anuncio WHERE FK_IDLoja = ?", (idLoja,))
        anuncios = self.banco.cur.fetchall()
        for anuncio in anuncios:
            idAnuncio = anuncio[0]
            self.excluirAnuncio(idAnuncio, banco)

        self.banco.cur.execute("UPDATE usuario SET FK_lojaUser = NULL WHERE FK_lojaUser = ?", (idLoja,))
        self.banco.cur.execute("UPDATE usuario SET tipoUsuario = ? WHERE FK_lojaUser = ?", ('COMPRADOR', idLoja))

        self.banco.cur.execute("DELETE FROM loja WHERE idLoja = ?", (idLoja,))
        self.banco.con.commit()

        self.loja.excluirLoja(banco)
        self.loja = None
    
    def excluirAnuncio(self, idAnuncio: int, banco: AcessoBanco):
        self.banco.cur.execute("DELETE FROM anuncio WHERE idAnuncio = ?", (idAnuncio,))
        self.banco.con.commit()
        for anuncio in self.loja.anuncios:
            if anuncio.idAnuncio == idAnuncio:
                anuncio.excluirAnuncio(banco)
                self.loja.anuncios.remove(anuncio)
                break
    
    def excluirProduto(self, idProduto: int, banco: AcessoBanco):
        self.banco.cur.execute("DELETE FROM produto WHERE idProduto = ?", (idProduto,))
        self.banco.con.commit()
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
        
    

    def recuperaAnuncios(self):
        self.banco.cur.execute("SELECT * FROM anuncio")
        anunciosBanco = self.banco.cur.fetchall()
        qntAnuncios = 0
        idsAnuncio = []
        categorias = []
        statusAnuncios = []
        idsProduto = []
        idsLoja = []
        
        
        for anuncio in anunciosBanco:
            idAnuncio, categoria, statusAnuncio, idProduto, idLoja = anuncio
            qntAnuncios += 1
            idsAnuncio.append(idAnuncio)
            categorias.append(categoria)
            statusAnuncios.append(statusAnuncio)
            idsProduto.append(idProduto)
            idsLoja.append(idLoja)

        return qntAnuncios, idsAnuncio, categorias, statusAnuncios, idsProduto, idsLoja

    def recuperaProdutos(self):
        self.banco.cur.execute("SELECT * FROM produto")
        produtosBanco = self.banco.cur.fetchall()
        qntProdutos = 0
        idsProduto = []
        nomesProduto = []
        descricoesProduto = []
        precos = []
        estoques = []
        idsLoja = []
        
        
        for produto in produtosBanco:
            idProduto, nome, descricao, preco, estoque, idLoja = produto
            qntProdutos += 1
            idsProduto.append(idProduto)
            nomesProduto.append(nome)
            descricoesProduto.append(descricao)
            precos.append(preco)
            estoques.append(estoque)
            idsLoja.append(idLoja)
            
        
        return qntProdutos, idsProduto, nomesProduto, descricoesProduto, precos, estoques, idsLoja


    def recuperaLoja(self, idLoja: int, idUsuario):
        nomeLoja, endereco, descricaoLoja = self.banco.recuperaLoja(idLoja)
        self.loja = Loja(nomeLoja, endereco, descricaoLoja, idUsuario)
        self.loja.idLoja = idLoja
        return nomeLoja, endereco, descricaoLoja
    
    
    def recuperaProdutosUser(self, idLoja):
        self.banco.cur.execute("SELECT * FROM produto WHERE FK_Loja = ?", (idLoja,))
        produtosBanco = self.banco.cur.fetchall()
        qntProdutos = 0
        idsProduto = []
        nomesProduto = []
        descricoesProduto = []
        precos = []
        estoques = []
        
        
        for produto in produtosBanco:
            idProduto, nome, descricao, preco, estoque, idLoja = produto
            qntProdutos += 1
            idsProduto.append(idProduto)
            nomesProduto.append(nome)
            descricoesProduto.append(descricao)
            precos.append(preco)
            estoques.append(estoque)
            
            newProduto = Produto(nome, descricao, preco, estoque, idLoja)
            newProduto.idProduto = idProduto
            self.loja.produtos.append(newProduto)
            
        
        return qntProdutos, idsProduto, nomesProduto, descricoesProduto, precos, estoques, idLoja
    
    def recuperaAnunciosUser(self, idLoja: int):
        self.banco.cur.execute("SELECT * FROM anuncio WHERE FK_idLoja = ?", (idLoja,))
        anunciosBanco = self.banco.cur.fetchall()
        qntAnuncios = 0
        idsAnuncio = []
        categorias = []
        status = []
        idsProduto = []        
        
        for anuncio in anunciosBanco:
            idAnuncio, categoria, statusAnuncio, idProduto, idLoja = anuncio
            qntAnuncios += 1
            idsAnuncio.append(idAnuncio)
            categorias.append(categoria)
            status.append(statusAnuncio)
            idsProduto.append(idProduto)
            
            newAnuncio = Anuncio(idProduto, idLoja, categoria, status)
            newAnuncio.idAnuncio = idAnuncio
            self.loja.anuncios.append(newAnuncio)
        
        return qntAnuncios, idsAnuncio, categorias, status, idsProduto

    def recuperaCarrinho(self, idUsuario):
        self.banco.cur.execute("SELECT FK_carrinho FROM usuario WHERE idUsuario = ?", (idUsuario,))
        result = self.banco.cur.fetchone()
        if not result:
            return None, 0
        idCarrinho = result[0]

        self.banco.cur.execute("SELECT total FROM carrinho WHERE idCarrinho = ?", (idCarrinho,))
        carrinho = self.banco.cur.fetchone()
        if not carrinho or carrinho[0] is None:
            return idCarrinho, 0
        total = carrinho[0]
        return idCarrinho, total
    
    
    def recuperaItens(self, idCarrinho):
        if idCarrinho is None:
            return 0, [], [], []
        self.banco.cur.execute("SELECT * FROM item WHERE FK_idCarrinho = ?", (idCarrinho,))
        itensBanco = self.banco.cur.fetchall()
        qntItem = 0
        idsItem = []
        idsProduto = []
        quantidades = []
        
        for item in itensBanco:
            idItem, fk_idCarrinho, fk_produto, quantidade = item
            qntItem += 1
            idsItem.append(idItem)
            idsProduto.append(fk_produto)
            quantidades.append(quantidade)

        return qntItem, idsItem, idsProduto, quantidades
