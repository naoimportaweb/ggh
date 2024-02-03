
# criar tabelas e campos.

CREATE TABLE cliente ( id varchar(255) NOT NULL, jid varchar(255) unique, public_key TEXT, apelido varchar(255) unique, pontuacao int,
  PRIMARY KEY(id) );

CREATE TABLE grupo ( id varchar(255) NOT NULL, jid varchar(255) unique, nome varchar(255), descricao TEXT,
  PRIMARY KEY(id) );

CREATE TABLE grupo_cliente ( id_grupo varchar(255) NOT NULL, id_cliente varchar(255) NOT NULL,
  PRIMARY KEY(id_grupo, id_cliente) );

CREATE TABLE nivel ( id varchar(255) NOT NULL, nome varchar(255), id_grupo varchar(255), posicao int, pontuacao int, tempo int,
  PRIMARY KEY(id) );

CREATE TABLE tag ( id varchar(255) NOT NULL, nome varchar(255), id_grupo varchar(255),
  PRIMARY KEY(id) );

CREATE TABLE nivel_cliente ( id_cliente varchar(255) NOT NULL, id_nivel varchar(255) NOT NULL,
  PRIMARY KEY(id_cliente, id_nivel) );

CREATE TABLE tag_cliente ( id_cliente varchar(255) NOT NULL, id_tag varchar(255) NOT NULL,
  PRIMARY KEY(id_cliente, id_tag) );

CREATE TABLE mensagem( id varchar(255) NOT NULL, id_remetente varchar(255), id_destinatario varchar(255),
  mensagem_criptografada LONGTEXT, chave_simetrica_criptografada TEXT, data_hora_envio datetime, ordem varchar(255),
  PRIMARY KEY(id) );

CREATE TABLE mensagem_nivel ( id_nivel varchar(255) NOT NULL, id_mensagem varchar(255) NOT NULL,
  PRIMARY KEY(id_nivel, id_mensagem) );

# relacionamento
ALTER TABLE grupo_cliente ADD FOREIGN KEY (id_grupo) REFERENCES grupo(id); 
ALTER TABLE grupo_cliente ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id); 
ALTER TABLE nivel_cliente ADD FOREIGN KEY (id_nivel) REFERENCES nivel(id); 
ALTER TABLE nivel_cliente ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id); 
ALTER TABLE tag_cliente ADD FOREIGN KEY (id_tag) REFERENCES tag(id); 
ALTER TABLE tag_cliente ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id); 
ALTER TABLE mensagem_nivel ADD FOREIGN KEY (id_mensagem) REFERENCES mensagem(id); 
ALTER TABLE mensagem_nivel ADD FOREIGN KEY (id_nivel) REFERENCES nivel(id); 
ALTER TABLE nivel ADD FOREIGN KEY (id_grupo) REFERENCES grupo(id); 
ALTER TABLE tag ADD FOREIGN KEY (id_grupo) REFERENCES tag(id); 
ALTER TABLE mensagem ADD FOREIGN KEY (id_remetente) REFERENCES cliente(id); 
ALTER TABLE mensagem ADD FOREIGN KEY (id_destinatario) REFERENCES cliente(id); 

# carga de dados iniciais par um projeto exemplo
insert into grupo(id, jid, nome, descricao) values("a9744c19ff882ebb9058a3c5096e6000", "nao.importa.web@jabb3r.de", "DEV Cypherpunk", "");
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("1", "a9744c19ff882ebb9058a3c5096e6000", "Iniciante",  0,         0,        30);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("2", "a9744c19ff882ebb9058a3c5096e6000", "Anarquista", 10,        1000,     90);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("3", "a9744c19ff882ebb9058a3c5096e6000", "Cypher programmer", 20, 10000,    180);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("4", "a9744c19ff882ebb9058a3c5096e6000", "CypherPunk", 30,        -1,       365);
insert into grupo_cliente(id_cliente, id_grupo) values ("91d0cf8f3883a0dcb338d15a47b326c9", "a9744c19ff882ebb9058a3c5096e6000");
insert into nivel_cliente(id_cliente, id_nivel) values ("91d0cf8f3883a0dcb338d15a47b326c9", "4" );