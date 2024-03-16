
# criar tabelas e campos.
CREATE TABLE cliente ( id varchar(255) NOT NULL, jid varchar(255) unique, public_key LONGTEXT, apelido varchar(255) unique, pontuacao int,
  chave_simetrica_criptografada LONGTEXT,  PRIMARY KEY(id) );

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
   id_grupo varchar(255) NOT NULL, titulo varchar(255), tags varchar(255), descricao LONGTEXT, texto LONGTEXT, status int not null, ultima_alteracao varchar(255),
  PRIMARY KEY(id) );

CREATE TABLE conhecimento_tag ( id_tag varchar(255) NOT NULL, id_conhecimento varchar(255) NOT NULL,
  PRIMARY KEY(id_conhecimento, id_tag) );

CREATE TABLE conhecimento_status (id int not null, nome varchar(255), PRIMARY KEY(id) );

CREATE TABLE atividade(id varchar(255) NOT NULL, id_cliente varchar(255) NOT NULL,
  id_grupo varchar(255) NOT NULL, id_nivel varchar(255) NOT  NULL, id_status int DEFAULT 0,
  titulo varchar(255) NOT NULL, atividade LONGTEXT, execucoes INT DEFAULT 1, tentativas INT DEFAULT 3,
  instrucao_correcao LONGTEXT NOT NULL, data_maxima DATE DEFAULT '2079-06-12',   
  instrucao LONGTEXT NOT NULL, pontos_maximo INT DEFAULT 1,
 PRIMARY KEY(id) );

CREATE TABLE atividade_cliente( id varchar(255) NOT NULL, id_atividade varchar(255) NOT NULL,
  id_cliente VARCHAR(255) NOT NULL, resposta LONGTEXT, id_avaliador VARCHAR(255) DEFAULT NULL,
  data DATETIME NOT NULL, 
  pontos INT DEFAULT NULL, data_avaliador DATETIME DEFAULT NULL, consideracao_avaliador LONGTEXT DEFAULT NULL,
  PRIMARY KEY(id) );

CREATE TABLE atividade_status (id int not null, nome varchar(255), PRIMARY KEY(id) );

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
ALTER TABLE conhecimento ADD FOREIGN KEY (status) REFERENCES conhecimento_status(id); 
ALTER TABLE atividade ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id);
ALTER TABLE atividade ADD FOREIGN KEY (id_status) REFERENCES atividade_status(id);
ALTER TABLE atividade ADD FOREIGN KEY (id_grupo) REFERENCES grupo(id);
ALTER TABLE atividade ADD FOREIGN KEY (id_nivel) REFERENCES nivel(id);
ALTER TABLE atividade_cliente ADD FOREIGN KEY (id_atividade) REFERENCES atividade(id);
ALTER TABLE atividade_cliente ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id);

# EXEMPLO DE GRUPO

delete from grupo_cliente;
delete from mensagem;
delete from mensagem_nivel;
delete from nivel;
delete from nivel_cliente;
delete from tag;
delete from html;
delete from tag_cliente;  
delete from conhecimento_tag;
delete from conhecimento;
delete from conhecimento_status;
delete from cliente;
delete from grupo;

insert into conhecimento_status(id, nome) values(0, "Em desenvolvimento");
insert into conhecimento_status(id, nome) values(1, "Aguardando aprovação");
insert into conhecimento_status(id, nome) values(2, "Aprovado");
insert into conhecimento_status(id, nome) values(3, "Reprovado");

insert into atividade_status(id, nome) values(0, "Em desenvolvimento");
insert into atividade_status(id, nome) values(1, "Em uso");
insert into atividade_status(id, nome) values(2, "Desativado");

# Carga de dados iniciais par um projeto exemplo
insert into grupo(id, jid, nome, descricao) values("a639ffc7a87856c52ea8b6a75dff4ff7", "database.xmpp@xmpp.jp", "DEV Cypherpunk", "");
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("41f38c9c2383f414db6ce99f50cff9ad8", "a639ffc7a87856c52ea8b6a75dff4ff7", "Iniciante",  0,         0,        30);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("117072decd99445b4973e81d67edc91e5", "a639ffc7a87856c52ea8b6a75dff4ff7", "Anarquista", 10,        1000,     90);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("81a01e3b7dbc24a468a8252eafeb91e9a", "a639ffc7a87856c52ea8b6a75dff4ff7", "Cypher programmer", 20, 10000,    180);
insert into nivel(id, id_grupo, nome, posicao, pontuacao, tempo) values ("516734dcbd0c44a6daddfb1c9dd034f70", "a639ffc7a87856c52ea8b6a75dff4ff7", "CypherPunk", 30,        -1,       365);

insert into html(id, nome, html, id_grupo) values ('regras.html'      ,'Regras','<html><body>Regras</body></html>',             "a639ffc7a87856c52ea8b6a75dff4ff7");
insert into html(id, nome, html, id_grupo) values ('recomendacao.html','Recomendação','<html><body>Recomendação</body></html>', "a639ffc7a87856c52ea8b6a75dff4ff7");

insert into tag(id, nome, sigla, id_grupo) values ('ed583d0879894266bb8916f9abce53bc', 'Aprovador Conhecimento', 'aprovador_conhecimento', 'a639ffc7a87856c52ea8b6a75dff4ff7');
insert into tag(id, nome, sigla, id_grupo) values ('fd583d0879894266bb8916f9abce53bc', 'Criar atividade', 'atividade_criar',               'a639ffc7a87856c52ea8b6a75dff4ff7');
insert into tag(id, nome, sigla, id_grupo) values ('dd583d0879894266bb8916f9abce53bc', 'Corrigir atividade', 'atividade_corrigir',         'a639ffc7a87856c52ea8b6a75dff4ff7');
insert into tag(id, nome, sigla, id_grupo) values ('hd583d0879894266bb8916f9abce53bc', 'Editar recomendacoes', 'recomendacao_editar',      'a639ffc7a87856c52ea8b6a75dff4ff7');

insert into tag_cliente(id_tag, id_cliente) values ('ed583d0879894266bb8916f9abce53bc', '91d0cf8f3883a0dcb338d15a47b326c9');
insert into tag_cliente(id_tag, id_cliente) values ('fd583d0879894266bb8916f9abce53bc', '91d0cf8f3883a0dcb338d15a47b326c9');
insert into tag_cliente(id_tag, id_cliente) values ('dd583d0879894266bb8916f9abce53bc', '91d0cf8f3883a0dcb338d15a47b326c9');
insert into tag_cliente(id_tag, id_cliente) values ('hd583d0879894266bb8916f9abce53bc', '91d0cf8f3883a0dcb338d15a47b326c9');
