import uuid, os, sys, hashlib, json;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import random

from classes.mysqlhelp import MysqlHelp

class Cliente:
    def __init__(self, jid, grupo, public_key=None):
        if jid == None or type(jid) != type("") or jid.strip() == "":
            raise Exception("JID do cliente tem que ser uma STRING.")
        self.id = hashlib.md5( jid.encode() ).hexdigest() ;
        self.jid = jid;
        self.public_key = public_key;
        self.chave_servidor = None;
        self.grupo = grupo;
        self.pontuacao = 0;
        self.id_nivel = "";
        self.apelido = None;   # vem do banco de dados, tem que iniciar.
        self.nivel_posicao = 0;
        # cliente não existe, então vamos criar os diretórios dele.
        self.path_cliente = self.grupo.path_grupo + "/clientes/" + hashlib.md5( self.jid.encode() ).hexdigest();
    
    def carregar(self):
        my = MysqlHelp();
        sqls = [];
        valuess = [];
        cadastro = my.datatable( "select * from cliente where jid = %s", [ self.jid ] );
        nivel_inicial = my.datatable("SELECT * FROM nivel WHERE posicao = %s and id_grupo = %s",[ 0, self.grupo.id ])[0];
        if len(cadastro) == 0:
            sqls.append("INSERT INTO cliente (id, jid, public_key, apelido, pontuacao) values( %s, %s, %s, %s, %s)");
            valuess.append(  [ self.id, self.jid, self.public_key, my.chave_string("cliente", "apelido", 8 ) , self.pontuacao ]  );
        grupo = my.datatable( "select * from grupo_cliente where id_grupo = %s and id_cliente = %s ", [  self.grupo.id, self.id ] );
        if len(grupo) == 0:
            sqls.append("INSERT INTO grupo_cliente(id_cliente, id_grupo) values (%s, %s)");
            valuess.append( [ self.id, self.grupo.id ] );
        nivel = my.datatable( "select ni.posicao as posicao from nivel_cliente as nic inner join nivel as ni on nic.id_nivel = ni.id where ni.id_grupo = %s and nic.id_cliente = %s order by ni.posicao desc", [ self.grupo.id, self.id ] );
        if len(nivel) == 0:
            sqls.append("INSERT INTO nivel_cliente(id_cliente, id_nivel) values (%s, %s)");
            valuess.append( [ self.id, nivel_inicial["id"] ] );
        
        if len(sqls) > 0:
            my.executes(sqls, valuess);
            cadastro = my.datatable( "select * from cliente where jid = %s", [ self.jid ] );
        
        self.apelido = cadastro[0]["apelido"];
        self.pontuacao = cadastro[0]["pontuacao"];
        if self.public_key != None:
            if cadastro[0]["public_key"] != self.public_key:
                my.execute("UPDATE cliente SET public_key= %s where id = %s ", [ self.public_key, self.id ]);
        else:
            self.public_key = cadastro[0]["public_key"];
        cadastro = my.datatable( "select ni.id as id_nivel, ni.posicao as posicao from nivel_cliente as nic inner join nivel as ni on nic.id_nivel = ni.id where ni.id_grupo = %s and nic.id_cliente = %s order by ni.posicao desc", [ self.grupo.id, self.id ] );
        if len(cadastro) > 0:
            self.nivel_posicao = cadastro[0]["posicao"];
            self.id_nivel = cadastro[0]["id_nivel"];
        #insert into nivel_cliente( id_cliente, id_nivel ) values( '8140652f47496a8cc66a435101de9023', (select id from nivel where id_grupo = 'a9744c19ff882ebb9058a3c5096e6000' and posicao=0 limit 1)  )
        my = None;                  
    
    def chave_publica_salvar(self, chave):
        self.public_key = chave;
        my = MysqlHelp();
        my.execute("UPDATE cliente SET public_key= %s where id = %s ", [ self.public_key, self.id ]);
        my = None;
    
    def posso_nivel(self, nivel_id):
        my = MysqlHelp();
        cadastro = my.datatable( "select ni.id as id_nivel, ni.posicao as posicao from nivel_cliente as nic inner join nivel as ni on nic.id_nivel = ni.id where ni.id = %s and ni.id_grupo = %s and nic.id_cliente = %s order by ni.posicao desc", [ nivel_id, self.grupo.id, self.id ] );
        if len(cadastro) > 0:
            return cadastro[0]["posicao"] <= self.nivel_posicao;
        return False;

