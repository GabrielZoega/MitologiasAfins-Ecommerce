CREATE TABLE IF NOT EXISTS usuario (
    idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeUsuario TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipoUsuario TEXT NOT NULL CHECK (tipoUsuario IN ('VENDEDOR', 'COMPRADOR')),
    FK_lojaUser INTEGER,
    FK_carrinho INTEGER NOT NULL,
    FOREIGN KEY (FK_lojaUser) REFERENCES loja (idLoja)
    FOREIGN KEY (FK_carrinho) REFERENCES carrinho (idCarrinho)
);

CREATE TABLE IF NOT EXISTS carrinho(
    idCarrinho INTEGER PRIMARY KEY AUTOINCREMENT,
    total INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS item(
    idItem INTEGER PRIMARY KEY AUTOINCREMENT,
    FK_idCarrinho INTEGER NOT NULL,
    FK_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (FK_idCarrinho) REFERENCES carrinho (idCarrinho),
    FOREIGN KEY (FK_produto) REFERENCES produto (idProduto)
);

CREATE TABLE IF NOT EXISTS loja (
    idLoja INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeLoja TEXT NOT NULL UNIQUE,
    endereco TEXT NOT NULL UNIQUE,
    descricaoLoja TEXT NOT NULL 
);

CREATE TABLE IF NOT EXISTS anuncio (
    idAnuncio INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL CHECK (categoria IN ('TESTE')),
    statusAnuncio TEXT NOT NULL CHECK (statusAnuncio IN ('ATIVO', 'PAUSADO')),
    FK_idProduto INTEGER NOT NULL UNIQUE,
    FK_idLoja INTEGER NOT NULL,
    FOREIGN KEY (FK_idProduto) REFERENCES produto (idProduto) ON DELETE CASCADE,
    FOREIGN KEY (FK_idLoja) REFERENCES loja (idLoja) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS produto (
    idProduto INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeProduto TEXT NOT NULL UNIQUE,
    descricaoProduto TEXT NOT NULL,
    preco DOUBLE NOT NULL,
    estoque INTEGER NOT NULL,
    FK_Loja INTEGER NOT NULL,
    FOREIGN KEY (FK_Loja) REFERENCES loja (idLoja) ON DELETE CASCADE
);