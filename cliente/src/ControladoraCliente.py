from PyQt6.QtCore import QObject, pyqtSignal
from Status import Status
from Categoria import Categoria
from Usuario import Usuario
from TipoCliente import TipoCliente
from Anuncio import Anuncio
from Produto import Produto
import Pyro5.api

#TODO acho que pode remover quase todos os return, verificar depois
#TODO não está atualizando as informações na tela quando criamos um anuncio

class ControladoraCliente(QObject):
    
    login_validado = pyqtSignal(bool, str)
    anuncios_recuperados = pyqtSignal(list)
    produtos_recuperados = pyqtSignal(list)
    anuncios_user_recuperados = pyqtSignal(list)
    produtos_user_recuperados = pyqtSignal(list)
    loja_criada = pyqtSignal(bool, str)
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

    def __init__(self):
        super().__init__()
        self.servidor = Pyro5.api.Proxy("PYRONAME:Servidor")
        self.usuario = Usuario()
        self.idCarrinho = None
        self.idLoja = None
        self.anuncios = []
        self.produtos = []


    # FUNÇÔES DE CRIAÇÃO
    def criarLoja(self, nomeLoja: str, descricaoLoja: str, endereco: str):
        try:
            print("CriarLoja -> Cliente\n")
            self.usuario.tipoCliente = TipoCliente.VENDEDOR
            self.idLoja = self.servidor.criarLoja(nomeLoja, endereco, descricaoLoja, self.usuario.idUser)
            self.loja_criada.emit(True)
        except Exception as e:
            print(f"Erro: {e}")
            if "nomeLoja" in str(e):
                self.loja_criada.emit(False, "Esse nome de loja já existe.")
            elif "endereco" in str(e):
                self.loja_criada.emit(False, "Esse endereco de loja já existe.")
            else:
                self.loja_criada.emit(False, "Erro ao criar a loja.")
        
    def criarAnuncio(self, categoria:Categoria, status:Status, idProduto:int):
        try:
            print("CriarAnuncio -> Cliente\n")
            self.anuncio_criado.emit("ok") #dps a gente como colocar erro
            return self.servidor.criarAnuncio(categoria, status, self.idLoja, idProduto)
        except Exception as e:
            print(f"Erro: {e}")
            if "FK_idProduto" in str(e):
                self.anuncio_criado.emit("Esse produto já está associado a um anúncio.")
            else:
                self.anuncio_criado.emit("Erro ao criar anúncio.")
    
    def criarProduto(self, nomeProduto:str, descricao:str, preco:float, estoque:int):
        try:
            print("CriarProduto -> Cliente\n")
            idProduto = self.servidor.criarProduto(nomeProduto, descricao, preco, estoque, self.idLoja)
            self.produto_criado.emit(idProduto, "Sucesso ao criar o produto.")
        except Exception as e:
            print(f"Erro: {e}")
            if "nomeProduto" in str(e):
                self.produto_criado.emit("-1", "Esse nome de produto já existe.")
            else:
                self.produto_criado.emit("-1", "Erro ao criar o produto.")
            


    # LOGIN E CADASTRO
    def cadastrarUsuario(self,nome:str,email:str,senha:str):
        print("CadastrarUsuario -> Cliente\n")
        try:
            idUsuario, idCarrinho = self.servidor.cadastrarUsuario(nome, email, senha)
            self.usuario.cadastrarUsuario(idUsuario, nome, email, senha, idCarrinho)
            self.login_validado.emit(True, "Usuário Cadastrado com Sucesso!")
            return idUsuario, idCarrinho
        except Exception as e:
            print(f"Erro: {e}")
            if "nomeUsuario" in str(e):
                self.login_validado.emit(False, "Esse nome de usuário já existe.")
            elif "email" in str(e):
                self.login_validado.emit(False, "Esse email já foi usado.")
            else:
                self.login_validado.emit(False, "Erro ao cadastrar o usuário.")
     
    def fazerLogin(self, email: str, senha:str):
        print("FazerLogin -> Cliente\n")
        response = self.servidor.fazerLogin(email, senha)
        print(response)
        if response == 403:
            self.login_validado.emit(False, "Email ou Senha incorreta")
        elif response == 0:
            self.login_validado.emit(False, "Usuário não cadastrado")
        else:
            idUsuario, nome, emailBanco, senhaBanco, tipoUsuario, idLoja, idCarrinho, tipoUsuario = response
            self.usuario.fazerLogin(idUsuario, nome, emailBanco, senhaBanco, idCarrinho, idLoja, tipoUsuario)
            self.login_validado.emit(True, "Sucesso no Login!")
            self.recuperaLoja(idLoja)
            self.recuperaAnunciosUser(idLoja)
            self.recuperaProdutosUser(idLoja)
    
    # RECUPERAM INFORMAÇÕES DO USUÁRIO
    def recuperaLoja(self, idLoja: int):
        print("RecuperaLoja -> Cliente\n")
        self.idLoja = idLoja
        return self.servidor.recuperaLoja(idLoja)
    
    def recuperaProdutosUser(self, idLoja: int):
        print("RecuperaProdutosUser -> Cliente\n")
        qntProdutos, idsProduto, nomesProduto, descricoesProduto, precos, estoques, idLoja = self.servidor.recuperaProdutosUser(idLoja)
        produtos = []
        
        for i in range (qntProdutos):
            produto = Produto(idsProduto[i], nomesProduto[i], descricoesProduto[i], precos[i], estoques[i], idLoja)
            produtos.append(produto)
            
        self.produtos_user_recuperados.emit(produtos)
        
    
    def recuperaAnunciosUser(self, idLoja: int):
        print("RecuperaAnunciosUser -> Cliente\n")
        qntAnuncios, idsAnuncio, categorias, status, idsProduto = self.servidor.recuperaAnunciosUser(idLoja)
        anuncios = []
        
        for i in range (qntAnuncios):
            anuncio = Anuncio(idsProduto[i], categorias[i], Status[status[i]], idsAnuncio[i], idLoja)
            anuncios.append(anuncio)
                                
        self.anuncios_user_recuperados.emit(anuncios)
        
    
    def recuperaCarrinho(self, idUsuario: int):
        print("RecuperaCarrinho -> Cliente\n")
        return self.servidor.recuperaCarrinho(idUsuario)
        
    def recuperaItens(self, idCarrinho: int):
        print("RecuperaItens -> Cliente\n")
        return self.servidor.recuperaItens(idCarrinho)
    
    
    # FUNÇÕES DE EXCLUSÃO
    def excluirLoja(self, idLoja:int):
        print("ExcluirLoja -> Cliente\n")
        self.servidor.excluirLoja(idLoja)
        self.idLoja = None
        self.loja_excluida.emit("Loja excluída com sucesso")
    
    def excluirAnuncio(self,idAnuncio:int):
        print("ExcluirAnuncio -> Cliente\n")
        self.servidor.excluirAnuncio(idAnuncio)
        self.anuncio_excluido.emit(idAnuncio)
                
    def excluirProduto(self,idProduto:int):
        print("ExcluirProduto -> Cliente\n")
        self.servidor.excluirProduto(idProduto)


    # FUNÇÕES DE ALTERAÇÃO DA LOJA
    def alterarNomeLoja(self,nomeLoja:str, idLoja: int):
        print("AlterarNomeLoja -> Cliente\n")
        self.servidor.alterarNomeLoja(nomeLoja, idLoja)
        self.nome_loja_alterado.emit(nomeLoja)
        
    def alterarEndereco(self,endereco:str, idLoja: int):
        print("AlterarEndereco -> Cliente\n")
        self.servidor.alterarEndereco(endereco, idLoja)
        self.endereco_loja_alterado.emit(endereco)
            
    def alterarDescricaoLoja(self,descricao:str, idLoja: int):
        print("AlterarDescricaoLoja -> Cliente\n")
        self.servidor.alterarDescricaoLoja(descricao, idLoja)
        self.descricao_loja_alterada.emit(descricao)


    # FUNÇÕES DE ALTERAÇÃO DO ANUNCIO
    def alterarCategoria(self,idAnuncio:int, categoria: Categoria):
        print("AlterarCategoria -> Cliente\n")
        self.servidor.alterarCategoria(idAnuncio, categoria)
        self.categoria_anuncio_alterada.emit(categoria.value)
   
    def alterarStatus(self,idAnuncio:int, status:Status):
        print("AlterarStatus -> Cliente\n") 
        self.servidor.alterarStatus(idAnuncio, status)
        self.visibilidade_anuncio_alterada.emit(status.name)

    def alterarProduto(self,idAnuncio:int, idProduto:int):
        print("AlterarProduto -> Cliente\n")
        self.servidor.alterarProduto(idAnuncio, idProduto)


    # FUNÇÕES DE ALTERAÇÃO DO PRODUTO
    def alterarNomeProduto(self, idProduto:int, nome: str):
        print("AlterarNomeProduto -> Cliente\n")
        self.servidor.alterarNomeProduto(idProduto, nome)
        self.nome_produto_alterado.emit(nome)
    
    def alterarDescricaoProduto(self, idProduto:int, descricaoProduto: str):
        print("AlterarDescricaoProduto -> Cliente\n")
        self.servidor.alterarDescricaoProduto(idProduto, descricaoProduto)
        self.descricao_produto_alterada.emit(descricaoProduto)

    def alterarPrecoProduto (self, idProduto:int, preco:float):
        print("AlterarPrecoProduto -> Cliente\n")
        self.servidor.alterarPreco(idProduto, preco)
        self.preco_produto_alterado.emit(preco)
        
    def alterarEstoqueProduto (self,idProduto:int, estoque: int):
        print("AlterarEstoqueProduto -> Cliente\n")
        self.servidor.alterarEstoque(idProduto, estoque)
        self.estoque_produto_alterado.emit(estoque)
    
    
    # FUNÇÕES DO CARRINHO
    def adicionarItem(self,idCarrinho:int,idProduto:int,quantidade:int):
        print("AdicionarItem -> Cliente\n")
        return self.servidor.adicionarItem(idCarrinho, idProduto, quantidade)
    
    def alterarQuantidade(self,idItem:int, quantidade:int):
        print("AlterarQuantidade -> Cliente\n") 
        self.servidor.alterarQuantidade(idItem, quantidade)
    
    def fecharCarrinho(self, idCarrinho):
        print("FecharCarrinho -> Cliente\n")    
        return self.servidor.fecharCarrinho(idCarrinho)
    
    
    # RECUPARAÇÃO DE INFORMAÇÕES DO BANCO
    def recuperaAnuncios (self):
        print("RecuperaAnuncios -> Cliente\n")
        qntAnuncios, idsAnuncio, categorias, statusAnuncio, idsProduto, idsLoja = self.servidor.recuperaAnuncios()
        
        self.anuncios.clear()
        for i in range (qntAnuncios):
            anuncio = Anuncio(idsProduto[i], categorias[i], Status[statusAnuncio[i]], idsAnuncio[i], idsLoja[i])
            self.anuncios.append(anuncio)
            
        self.anuncios_recuperados.emit(self.anuncios)
            
    def recuperaProdutos(self):
        print("RecuperaProdutos -> Cliente\n")
        qntProdutos, idsProdutos, nomes, descricoes, precos, estoques, idsLoja = self.servidor.recuperaProdutos()
        
        self.produtos.clear()
        for i in range (qntProdutos):
            produto = Produto(idsProdutos[i], nomes[i], descricoes[i], precos[i], estoques[i], idsLoja[i])
            self.produtos.append(produto)
        
        self.produtos_recuperados.emit(self.produtos)