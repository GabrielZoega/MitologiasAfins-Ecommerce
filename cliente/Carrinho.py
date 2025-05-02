class Carrinho():
    def __init__(self):
        self.itens = [] # Essa é uma lista do tipo itens
        self.idCarrinho = 0
        
    def adicionarItem (self, item):
        self.itens.append(item)
        
    def removerItem (self, item):
        for i in self.itens:
            if i == item:
                self.itens.remove(i)
                print(f"Item '{i}' removido do carrinho.")
                return
        print(f"Item '{i}' não encontrado no carrinho.")
        
    def mostrarItens(self):
        if not self.itens:
            print("Carrinho vazio.")
        else:
            for i in self.itens:
                print(i)   
                