class Carrinho():
    def __init__(self):
        self.itens = [] # Essa é uma lista do tipo itens
        self.idCarrinho = 0
        self.total = 0.0
        
    def adicionarItem (self, item):
        self.itens.append(item)
        item.quantidadeCarrinho = 1
        
    def removerItem (self, item):
        for i in self.itens:
            if i == item: # comparar nomes
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
    
    def calcularPrecoTotal(self): # percorre os itens do carrinho multiplicando o preço preço pela quantidade
        for item in self.itens:
            self.total += item.precoItem * item.quantidadeCarrinho

 ##   def aumentarQuantidadeItens(self, item): #Essa função serve para poder aumentar a quantidade de um certo item no carrinho
   ##     for i in self.itens: # verificar como fazer esse for melhor
     #       if i == item:
      #         return
       # print(f"Item '{i}' não encontrado no carrinho.")

#def diminuirQuantidadeItens(self, item): #Essa função serve para poder aumentar a quantidade de um certo item no carrinho
 #       for i in self.itens:
  #          if i == item:
   #             self.itens.remove(i)
    #            print(f"Item '{i}' removido do carrinho.")
     #           return
      #  print(f"Item '{i}' não encontrado no carrinho.")

                