from Item import Item

class Carrinho():
    def __init__(self,idCarrinho:int):
        self.itens = []
        self.idCarrinho = idCarrinho
#       self.total = 0.0
        
    def adicionarItem (self, idProduto:int, precoItem:float,quantidade:int,idItem:int):
        self.itens.append(Item(idProduto,precoItem,idItem,quantidade))
         
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
            total += item.precoItem * item.quantidadeCarrinho
        return total

    def alterarQuantidade(self,quantidade:int,idItem:int):
        for itens in self.itens:
            if itens.idItem == idItem:
                if quantidade == 0:
                    self.removerItem(itens.idProduto)
                else:
                    itens.quantidadeCarrinho = quantidade
        
    def fecharCarrinho(self,idCarrinho:int): 
        print(f"Preço total: {self.calcularPrecoTotal()}")
        self.itens = []
        # mandar solicitação para o back para ver se todos os itens no carrinho estão disponiveis
        # mandar para o back tirar os itens totais do estoque
        