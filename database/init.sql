CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);

-- Isso aqui não vai ter no arquivo init de verdade, a gente aqui só vai criar as tabelas
INSERT INTO usuario (nome, email, senha) VALUES ('Gabriel', 'gabriel@gmail.com', 'teste123')