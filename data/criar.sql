
# criar tabelas e campos.

CREATE TABLE cliente ( id varchar(255) NOT NULL, jid varchar(255) unique, public_key TEXT, apelido varchar(255) unique, pontuacao int,
  PRIMARY KEY(id) );

CREATE TABLE grupo ( id varchar(255) NOT NULL, jid varchar(255) unique, nome varchar(255), descricao TEXT,
  PRIMARY KEY(id) );

CREATE TABLE grupo_cliente ( id_grupo varchar(255) NOT NULL, id_cliente varchar(255) NOT NULL,
  PRIMARY KEY(id_grupo, id_cliente) );

CREATE TABLE nivel ( id varchar(255) NOT NULL, nome varchar(255), id_grupo varchar(255), posicao int, pontuacao int, tempo int,
  PRIMARY KEY(id) );

CREATE TABLE tag ( id varchar(255) NOT NULL, nome varchar(255), sigla varchar(255), id_grupo varchar(255),
  PRIMARY KEY(id) );

CREATE TABLE html ( id varchar(255) NOT NULL, nome varchar(255), id_grupo varchar(255), html LONGTEXT,
  PRIMARY KEY(id) );

CREATE TABLE nivel_cliente ( id_cliente varchar(255) NOT NULL, id_nivel varchar(255) NOT NULL,
  PRIMARY KEY(id_cliente, id_nivel) );

CREATE TABLE tag_cliente ( id_cliente varchar(255) NOT NULL, id_tag varchar(255) NOT NULL,
  PRIMARY KEY(id_cliente, id_tag) );

CREATE TABLE mensagem( id varchar(255) NOT NULL, id_remetente varchar(255), id_destinatario varchar(255),
  mensagem_criptografada LONGTEXT, chave_simetrica_criptografada LONGTEXT, data_hora_envio datetime, ordem varchar(255),
  PRIMARY KEY(id) );

CREATE TABLE mensagem_nivel ( id_nivel varchar(255) NOT NULL, id_mensagem varchar(255) NOT NULL,
  PRIMARY KEY(id_nivel, id_mensagem) );

CREATE TABLE conhecimento ( id varchar(255) NOT NULL, id_cliente varchar(255) NOT NULL, id_revisor varchar(255) DEFAULT NULL,  id_nivel varchar(255) NOT NULL,
   id_grupo varchar(255) NOT NULL, titulo varchar(255), tags varchar(255), descricao LONGTEXT, texto LONGTEXT, status int not null, 
  PRIMARY KEY(id) );

CREATE TABLE conhecimento_tag ( id_tag varchar(255) NOT NULL, id_conhecimento varchar(255) NOT NULL,
  PRIMARY KEY(id_conhecimento, id_tag) );

# relacionamento
ALTER TABLE grupo_cliente ADD FOREIGN KEY (id_grupo) REFERENCES grupo(id); 
ALTER TABLE grupo_cliente ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id); 
ALTER TABLE nivel_cliente ADD FOREIGN KEY (id_nivel) REFERENCES nivel(id); 
ALTER TABLE nivel_cliente ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id); 
ALTER TABLE tag_cliente ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id); 
ALTER TABLE mensagem_nivel ADD FOREIGN KEY (id_mensagem) REFERENCES mensagem(id); 
ALTER TABLE mensagem_nivel ADD FOREIGN KEY (id_nivel) REFERENCES nivel(id); 
ALTER TABLE nivel ADD FOREIGN KEY (id_grupo) REFERENCES grupo(id); 
ALTER TABLE tag ADD FOREIGN KEY (id_grupo) REFERENCES grupo(id); 
ALTER TABLE html ADD FOREIGN KEY (id_grupo) REFERENCES grupo(id); 
ALTER TABLE mensagem ADD FOREIGN KEY (id_remetente) REFERENCES cliente(id); 
ALTER TABLE mensagem ADD FOREIGN KEY (id_destinatario) REFERENCES cliente(id); 
ALTER TABLE conhecimento_tag ADD FOREIGN KEY (id_conhecimento) REFERENCES conhecimento(id); 
ALTER TABLE conhecimento_tag ADD FOREIGN KEY (id_tag) REFERENCES tag(id); 

# EXEMPLO DE GRUPO
delete from cliente;
delete from grupo;
delete from grupo_cliente;
delete from mensagem;
delete from mensagem_nivel;
delete from nivel;
delete from nivel_cliente;
delete from tag;
delete from tag_cliente;  

# Carga de dados iniciais par um projeto exemplo
insert into grupo(id, jid, nome, descricao) values("1b89816ae9df5dc039242b4899fb06a1", "cypherpunkgroup@jabber.sa", "DEV Cypherpunk", "");
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("41f38c9c2383f414db6ce99f50cff9ad8", "1b89816ae9df5dc039242b4899fb06a1", "Iniciante",  0,         0,        30);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("117072decd99445b4973e81d67edc91e5", "1b89816ae9df5dc039242b4899fb06a1", "Anarquista", 10,        1000,     90);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("81a01e3b7dbc24a468a8252eafeb91e9a", "1b89816ae9df5dc039242b4899fb06a1", "Cypher programmer", 20, 10000,    180);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("516734dcbd0c44a6daddfb1c9dd034f70", "1b89816ae9df5dc039242b4899fb06a1", "CypherPunk", 30,        -1,       365);
insert into html(id, nome, html) values ('regras.html','Regras','<html><body>Regras</body></html>');
insert into html(id, nome, html) values ('recomendacao.html','Recomendação','<html><body>Recomendação</body></html>');
insert into tag(id, nome, sigla, id_grupo) values ('ed583d0879894266bb8916f9abce53bc', 'Aprovador Conhecimento', 'aprovador_conhecimento', '1b89816ae9df5dc039242b4899fb06a1');
insert into tag_cliente(id_tag, id_cliente) values ('ed583d0879894266bb8916f9abce53bc', '8140652f47496a8cc66a435101de9023');
