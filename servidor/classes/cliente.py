import uuid, os, sys, hashlib, json, time, traceback;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import random

from datetime import datetime
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
        self.pontuacao_data_processamento = datetime.now().isoformat();
        self.path_cliente = self.grupo.path_grupo + "/clientes/" + hashlib.md5( self.jid.encode() ).hexdigest();
        self.tags = [];
    
    def definir_chave_servidor(self):
        my = MysqlHelp();
        self.chave_servidor = str( uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())) )[0:16];
        sql = "UPDATE cliente SET chave_servidor=%s where id=%s";
        my.execute(sql, [ self.chave_servidor, self.id ])
    def fromJson(self, js):
        self.id = js["id"];
        if js["chave_servidor"] != None and js["chave_servidor"] != "":
            self.chave_servidor = js["chave_servidor"];
        else:
            self.definir_chave_servidor();
        self.jid = js["jid"];
        self.id_nivel = js["id_nivel"];
        self.public_key = js["public_key"];
        self.apelido = js["apelido"];
        self.pontuacao = js["pontuacao"];
        self.pontuacao_data_processamento = js["pontuacao_data_processamento"];
        self.carregar_tag();
        self.carregar_nivel();

    def existo(self):
        my = MysqlHelp();
        return len(my.datatable( "select id from cliente where jid = %s", [ self.jid ] )) > 0;
    
    def registra_entrada(self):
        my = MysqlHelp();
        return len(my.datatable( "UPDATE cliente set data_acesso = %s where id=%s", [ datetime.now().isoformat(), self.id ] )) > 0;
    
    def carregar(self):
        try:
            if not self.existo():
                if not self.criar():
                    raise Exception("Não foi possível criar o cadastro."); 
            my = MysqlHelp();
            cadastro = my.datatable( "select * from cliente where jid = %s", [ self.jid ] )[0];
            self.fromJson( cadastro );
            return True;
        except:
            traceback.print_exc();
        return False;
    
    def carregar_nivel(self):
        my = MysqlHelp();
        cadastro = my.datatable( "select * from nivel as ni where ni.id_grupo = %s and ni.id = %s", [ self.grupo.id, self.id_nivel ] );
        self.nivel_posicao = cadastro[0]["posicao"];
    
    def carregar_tag(self):
        my = MysqlHelp();
        self.tags = my.datatable( "select tg.nome, tg.sigla from tag_cliente as tc inner join tag as tg on tc.id_tag = tg.id where tc.id_cliente = %s", [ self.id ] );
        
    def criar(self):
        my = MysqlHelp();
        sqls = [];
        valuess = [];
        try:
            self.pontuacao_data_processamento = datetime.now().isoformat();
            self.pontuacao = 0;
            
            nivel_inicial = my.datatable("SELECT * FROM nivel WHERE posicao = %s and id_grupo = %s",[ 0, self.grupo.id ])[0];

            sqls.append("INSERT INTO cliente (id, jid, public_key, apelido, pontuacao, pontuacao_data_processamento, id_nivel, data_cadastro, data_acesso) values( %s, %s, %s, %s, %s, %s, %s, %s, %s)");
            valuess.append(  [ self.id, self.jid, self.public_key, my.chave_string("cliente", "apelido", 8 ) , self.pontuacao, self.pontuacao_data_processamento, nivel_inicial["id"], self.pontuacao_data_processamento, self.pontuacao_data_processamento ]  );

            sqls.append("INSERT INTO grupo_cliente(id_cliente, id_grupo) values (%s, %s)");
            valuess.append( [ self.id, self.grupo.id ] );

            my.executes(sqls, valuess);
            my = None;           
            return True;
        except:
            traceback.print_exc();
        return False;       
    
    def chave_publica_salvar(self, chave):
        
        self.public_key = chave;
        my = MysqlHelp();
        my.execute("UPDATE cliente SET public_key= %s where id = %s ", [ self.public_key, self.id ]);
        my = None;
    
    def posso_nivel(self, nivel_id):
        my = MysqlHelp();
        cadastro = my.datatable(  "select * from nivel as ni where ni.id = %s and ni.id_grupo= %s", [ nivel_id, self.grupo.id ] );
        if len(cadastro) > 0:
            return cadastro[0]["posicao"] <= self.nivel_posicao;
        return False;
    
    def posso_tag(self, sigla):
        my = MysqlHelp();
        sql = "SELECT tg.* FROM tag  as tg inner join tag_cliente as tgc on tg.id = tgc.id_tag where tg.sigla = %s and tgc.id_cliente =  %s";
        cadastro = my.datatable( sql, [ sigla, self.id ] );
        if len(cadastro) > 0:
            return True;
        return False;

        values = [ cliente.id ];
        tag = my.datatable(sql, values);
        if len(tag) == 0:
            return {"status" : False, "erro" : "Não tem permissão para aprovar."};