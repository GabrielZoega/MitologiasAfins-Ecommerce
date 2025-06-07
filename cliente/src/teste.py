import Pyro5.api

name = input("Digite seu nome: ").strip()

EndPointServidor = Pyro5.api.Proxy("PYRONAME:Teste")
print(EndPointServidor.getMessage(name))