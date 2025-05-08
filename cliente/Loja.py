class Loja():
    def __init__(self, idLoja,nome,endereco,descricao):
        self.idLoja = idLoja
        self.nome = nome
        self.endereco = endereco
        self.descricao = descricao
        self.anuncios = []
        
    def alterarIdLoja(self,idLoja):
        self.idLoja = idLoja
        
    def alterarNome(self,nome):
        self.nome = nome
        
    def alterarEndereco (self,endereco):
        self.endereco = endereco
    
    def alterarDescricao (self,descricao):
        self.descricao = descricao
    
    def alterarAnuncio (self, idAnuncio, funcaoASerChamada, oQueAltera):
        for anuncio in self.anuncios:
            if anuncio.idAnuncio == idAnuncio:
               anuncio.alterarAnuncio(funcaoASerChamada, oQueAltera) 