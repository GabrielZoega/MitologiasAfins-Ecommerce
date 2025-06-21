from Categoria import Categoria
from Status import Status
from AcessoBanco import AcessoBanco
import sqlite3
import Pyro5.api

# Iniciara o processamento da tarefa requerida pelo cliente
@Pyro5.api.expose
class ControladoraServidor:
    
    def __init__(self):
        self.banco = AcessoBanco()
    
    # Operações de Criação:
    def criarLoja(self, nome: str, endereco: str, descricao: str, idUsuario: int):
        idLoja = self.banco.criarLoja(nome, endereco, descricao, idUsuario)
        return idLoja
    
    def criarAnuncio(self, categoria: Categoria, status: Status, idLoja: int, idProduto: int):
        idAnuncio = self.banco.criarAnuncio(categoria, status, idProduto, idLoja)
        return idAnuncio
    
    def criarProduto(self, nome: str, descricao: str, preco: float, estoque: int, idLoja: int):
        idProduto = self.banco.criarProduto(nome, descricao, preco, estoque, idLoja)
        return idProduto


    # Cadastro e Login
    def cadastrarUsuario(self, nome: str, email: str, senha: str):
        idCarrinho = self.banco.criarCarrinho()
        idUsuario = self.banco.cadastrarUsuario(nome, email, senha, idCarrinho)
        return idUsuario, idCarrinho
    
    def fazerLogin(self, email: str, senha: str):
        resultado = self.banco.recuperaLogin(email)
        if resultado is None:
            return 0
        idUsuario, nome, emailBanco, senhaBanco, tipoUsuario, idLoja, idCarrinho, tipoUsuario = resultado
        
        if senha != senhaBanco:
            return 403
        return idUsuario, nome, emailBanco, senhaBanco, tipoUsuario, idLoja, idCarrinho, tipoUsuario
    
    
    # Operações de Edição da Loja:
    def alterarNomeLoja(self, nome: str, idLoja: int):
        self.banco.alterarNomeLoja(nome, idLoja)
    
    def alterarEndereco(self, endereco: str, idLoja: int):
        self.banco.alterarEndereco(endereco, idLoja)
    
    def alterarDescricaoLoja(self, descricao: str, idLoja):
        self.banco.alterarDescricaoLoja(descricao, idLoja)
    
    
    # Operações de Edição do Anuncio
    def alterarCategoria(self, idAnuncio: int, categoria: Categoria):
        print(f"Categoria: {categoria}")
        self.banco.alterarCategoria(idAnuncio, categoria)
        
    def alterarStatus(self, idAnuncio: int, status: Status):
        print(f"Status: {Status(status).name}")
        self.banco.alterarStatus(idAnuncio, Status(status).name)
        
    def alterarProduto(self, idAnuncio: int, idProduto: int):
        print(f"Produto: {idProduto}")
        self.banco.alterarProduto(idAnuncio, idProduto)


    # Operações de Edição do Produto
    def alterarNomeProduto(self, idProduto: int, nome: str):
        print(f"Nome: {nome}")
        self.banco.alterarNomeProduto(idProduto, nome)
        
    def alterarDescricaoProduto(self, idProduto: int, descricao: str):
        print(f"Descricao: {descricao}")
        self.banco.alterarDescricaoProduto(idProduto, descricao)
                
    def alterarPreco(self, idProduto: int, preco: float):
        print(f"Preco: {preco}")
        self.banco.alterarPreco(idProduto, preco)
                
    def alterarEstoque(self, idProduto: int, estoque: int):
        print(f"Estoque: {estoque}")
        self.banco.alterarEstoque(idProduto, estoque)
        

    # Operações de Exclusão:
    def excluirLoja(self, idLoja: int):
        print(f"Excluindo loja: {idLoja}")
        self.banco.excluirLoja(idLoja)
    
    def excluirAnuncio(self, idAnuncio: int):
        print(f"Excluindo Anuncio: {idAnuncio}")
        self.banco.excluirAnuncio(idAnuncio)
    
    def excluirProduto(self, idProduto: int):
        print(f"Excluindo Produto: {idProduto}")
        self.banco.excluirProduto(idProduto)
    
    
    # Funções de edição do carrinho
    def adicionarItem(self, idCarrinho: int, idProduto: int, quantidade: int):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        idItem = self.banco.adicionarItem(idCarrinho, idProduto, quantidade)
        cur.execute("SELECT preco FROM produto WHERE idProduto = ?", (idProduto,))
        result = cur.fetchone()
        preco = result[0]
        
        con.commit()
        con.close()
    
        return idItem, preco
    
    def alterarQuantidade(self, idItem: int, quantidade: int):
        self.banco.alterarQuantidade(idItem, quantidade)
    
    def fecharCarrinho(self, idCarrinho: int):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        
        cur.execute("SELECT idItem, FK_produto, quantidade FROM item WHERE FK_idCarrinho = ?", (idCarrinho,))
        itens = cur.fetchall()

        for item in itens:
            idItem, idProduto, quantidade = item
            cur.execute("SELECT estoque FROM produto WHERE idProduto = ?", (idProduto,))
            estoque = cur.fetchone()[0]

            if quantidade > estoque:
                return 403

        for item in itens:
            idItem, idProduto, quantidade = item
            cur.execute("SELECT estoque FROM produto WHERE idProduto = ?", (idProduto,))
            estoque = cur.fetchone()[0]
            novoEstoque = estoque - quantidade

            self.alterarEstoque(idProduto, novoEstoque)
            cur.execute("DELETE FROM item WHERE idItem = ?", (idItem,))

        con.commit()
        con.close()
        return 200
        
    

    def recuperaAnuncios(self):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        
        cur.execute("SELECT * FROM anuncio")
        anunciosBanco = cur.fetchall()
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

        con.commit()
        con.close()
        return qntAnuncios, idsAnuncio, categorias, statusAnuncios, idsProduto, idsLoja

    def recuperaProdutos(self):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        
        cur.execute("SELECT * FROM produto")
        produtosBanco = cur.fetchall()
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
            
        con.commit()
        con.close()
        return qntProdutos, idsProduto, nomesProduto, descricoesProduto, precos, estoques, idsLoja


    def recuperaLoja(self, idLoja: int):
        nomeLoja, endereco, descricaoLoja = self.banco.recuperaLoja(idLoja)
        return nomeLoja, endereco, descricaoLoja
    
    
    def recuperaProdutosUser(self, idLoja: int):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        
        cur.execute("SELECT * FROM produto WHERE FK_Loja = ?", (idLoja,))
        produtosBanco = cur.fetchall()
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
        
        con.commit()
        con.close()
        return qntProdutos, idsProduto, nomesProduto, descricoesProduto, precos, estoques, idLoja
    
    def recuperaAnunciosUser(self, idLoja: int):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        
        cur.execute("SELECT * FROM anuncio WHERE FK_idLoja = ?", (idLoja,))
        anunciosBanco = cur.fetchall()
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
        
        con.commit()
        con.close()
        return qntAnuncios, idsAnuncio, categorias, status, idsProduto

    def recuperaCarrinho(self, idUsuario):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        
        cur.execute("SELECT FK_carrinho FROM usuario WHERE idUsuario = ?", (idUsuario,))
        result = cur.fetchone()
        if not result:
            return None, 0
        idCarrinho = result[0]

        cur.execute("SELECT total FROM carrinho WHERE idCarrinho = ?", (idCarrinho,))
        carrinho = cur.fetchone()
        if not carrinho or carrinho[0] is None:
            return idCarrinho, 0
        total = carrinho[0]
        
        con.commit()
        con.close()
        return idCarrinho, total
    
    
    def recuperaItens(self, idCarrinho):
        con = sqlite3.connect('../../database/maSql.db')
        cur = con.cursor()
        
        if idCarrinho is None:
            return 0, [], [], []
        cur.execute("SELECT * FROM item WHERE FK_idCarrinho = ?", (idCarrinho,))
        itensBanco = cur.fetchall()
        qntItem = 0
        idsItem = []
        idsProduto = []
        quantidades = []
        precos = []
        
        for item in itensBanco:
            idItem, fk_idCarrinho, fk_produto, quantidade = item
            qntItem += 1
            idsItem.append(idItem)
            idsProduto.append(fk_produto)
            quantidades.append(quantidade)
            cur.execute("SELECT preco FROM produto WHERE idProduto = ?", (fk_produto,))
            preco = cur.fetchone()
            preco = preco[0]
            preco = preco * quantidade
            precos.append(preco)
            
            
        con.commit()
        con.close()
        return qntItem, idsItem, idsProduto, quantidades, precos
    

if __name__ == "__main__":
    
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(ControladoraServidor)
    ns.register("Servidor", uri)
    
    print("Ready")
    daemon.requestLoop()
