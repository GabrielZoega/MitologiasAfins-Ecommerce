class Item():
    def __init__(self, nome, quantidadeTotal, precoItem):
        self.nome = nome
        self.quantidadeCarrinho = 0 # QUantidade de um item que tem no carrinho, exemplo 3 maçâs no carrinho
        self.quantidadeTotal = quantidadeTotal # Essa informação vem do servidor, quantidade total do item disponível, exemplo 50 maças
        self.precoItem = precoItem #valor do item, a maçã custa 10 reais-> informação vem do servidor
        
    