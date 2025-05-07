CREATE TABLE IF NOT EXISTS usuario (
    idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeUsuario TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    Fk_lojaUser INTEGER,
    FOREIGN KEY (Fk_lojaUser) REFERENCES loja (idLoja)
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
    Fk_idLoja INTEGER NOT NULL,
    FOREIGN KEY (FK_idProduto) REFERENCES produto (idProduto),
    FOREIGN KEY (Fk_idLoja) REFERENCES loja (idLoja)
);

CREATE TABLE IF NOT EXISTS produto (
    idProduto INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeProduto TEXT NOT NULL UNIQUE,
    descricaoProduto TEXT NOT NULL,
    preco DOUBLE NOT NULL,
    estoque INTEGER NOT NULL
);