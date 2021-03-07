drop database if exists erp;

create database erp;

use erp;

CREATE TABLE cadastros (
    nome VARCHAR(50) NOT NULL,
    senha VARCHAR(20) NOT NULL,
    nivel INT NOT NULL DEFAULT 1
);
 
insert into cadastros values ('admin', 'admin', 2);
 
drop table if exists produtos;
 
CREATE TABLE produtos (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ingredientes VARCHAR(1000),
    grupo VARCHAR(100),
    preco FLOAT
);
 
drop table if exists pedidos;
 
CREATE TABLE pedidos (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    ingredientes VARCHAR(1000),
    grupo VARCHAR(100),
    localEntrega VARCHAR(500),
    observacoes VARCHAR(1000)
);
 
SELECT 
    *
FROM
    produtos;
 
insert into pedidos (nome, ingredientes, grupo, localEntrega, observacoes) values ('pizza de mussarela', 'mussarela', 'pizzas', '', 'sem cebola');
insert into pedidos (nome, ingredientes, grupo, localEntrega, observacoes) values ('coca', '', 'bebidas', '', '');
 
drop table if exists estatisticaVendido;
 
CREATE TABLE estatisticaVendido (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    grupo VARCHAR(100),
    preco FLOAT
);