from Loja import Loja

# Iniciara o processamento da tarefa requerida pelo cliente
# Para decidir a operação, poderiamos ter um campo no JSON com essa informação
class ControladoraServidor:
    
    # Cria uma Loja por exemplo
    def criarLoja(self, nome, endereco, descricao):
        loja = Loja.__init__(nome, endereco, descricao)