from Item import Item

class Carrinho():
    def __init__(self):
        self.itens = []
        self.idCarrinho = 0
        self.total = 0.0
        
    def adicionarItem (self, item):
        item.quantidadeCarrinho = 1
        self.itens.append(item)
        
    def removerItem (self, idProduto):
        for item in self.itens:
            if item.idProduto == idProduto:
                self.itens.remove(item)
                print(f"Item '{item}' removido do carrinho.")
                return
        print(f"Item '{item}' não encontrado no carrinho.")
        
    def mostrarItens(self):
        if not self.itens:
            print("Carrinho vazio.")
        else:
            for item in self.itens:
                print(item)   
    
    def calcularPrecoTotal(self): # percorre os itens do carrinho multiplicando o preço preço pela quantidade
        for item in self.itens:
            self.total += item.precoItem * item.quantidadeCarrinho

    def aumentarQuantidadeItem(self, idProduto): #Essa função serve para poder aumentar a quantidade de um certo item no carrinho
        for item in self.itens: # verificar como fazer esse for melhor
            if item.idProduto == idProduto:
                item.quantidadeCarrinho = item.quantidadeCarrinho + 1
                return
            else:
                print(f"Item '{item}' não encontrado no carrinho.")

    def diminuirQuantidadeItem(self, idProduto): #Essa função serve para poder aumentar a quantidade de um certo item no carrinho
       for item in self.itens:
            if item.idProduto == idProduto:
               if item.quantidadeCarrinho == 1:
                   self.removerItem(idProduto)
                   return
               else: 
                   item.quantidadeCarrinho = item.quantidadeCarrinho - 1
                   return
            else:
                print(f"Item '{item}' não encontrado no carrinho.")

    def fecharCarrinho(self): 
        self.calcularPrecoTotal()
        # mandar solicitação para o back para ver se todos os itens no carrinho estão disponiveis
        # mandar para o back tirar os itens totais do estoque
        