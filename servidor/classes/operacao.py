import uuid, os, sys, hashlib, json, time, traceback;

from classes.mysqlhelp import MysqlHelp


class Operacao():
    def __init__(self):
        self.id = hashlib.md5( jid.encode() ).hexdigest() ;
        self.nome = None;
        self.id_grupo = None;
        self.id_operacao_status = None;
        self.data_inicio = None;
        self.data_fim = None;
        self.missao = None;
        self.foco = None;
        self.operacao_status = None;
        self.niveis = None;
        self.sigla = None;
        self.atividades = None;
    
    def carregar_capos(self, js):
        self.id = js["id"];
        self.nome = js["nome"];
        self.id_grupo = js["id_grupo"];
        self.id_operacao_status = js["id_operacao_status"];
        self.data_inicio = js["data_inicio"];
        self.data_fim = js["data_fim"];
        self.sigla = js["sigla"];
        self.missao = js["missao"];
        self.foco = js["foco"];
        return True;

    def carregar(self, id):
        my = MysqlHelp();
        elemento = my.datatable( "select * from operacao where id = %s", [self.id]);
        return carregar_capos( js );

    def carregar_niveis(self):
        my = MysqlHelp();
        self.niveis = my.datatable( "SELECT ni.id, ni.nome FROM nivel as ni inner join operacao_nivel as oni on ni.id = oni.id_nivel where oni.id_operacao = %s order by ni.posicao asc", [self.id]);
    def carregar_atividades(self):
        my = MysqlHelp();
        self.atividades = my.datatable( "SELECT atv.id, atv.titulo FROM atividade as atv inner join operacao_atividade as oatv on atv.id = oatv.id_atividade where oatv.id_operacao = %s", [self.id]);
    def carregar_status(self):
        my = MysqlHelp();
        self.operacao_status = my.datatable( "SELECT * from operacao_status where id=%s", [self.id_operacao_status])[0];
    def toJson(self):
        self.carregar_niveis();
        self.carregar_atividades();
        self.carregar_status();
        return {"id" : js["id"], "sigla" : js["sigla"], "nome" : js["nome"],"id_operacao_status" : js["id_operacao_status"],"nome_operacao_status" : self.operacao_status["nome"],"data_inicio" : js["data_inicio"],"data_fim" : js["data_fim"],"missao" : js["missao"],"foco" :  js["foco"], "atividades" : self.atividades, "niveis" : self.niveis };
    @stticmethod
    def listar(id_nivel):
        my = MysqlHelp();
        sql = "select op.* from operacao as op where op.id_nivel in (select id from nivel where posicao <= %s )";
        buffers = [];
        dados = my.datatable(sql, [id_nivel]);
        for row in dados:
            buffer = Operacao();
            buffer.carregar_capos(row);
            buffers.append( buffer );
        return buffers;
    @stticmethod
    def listar_json(id_nivel):
        buffers_json = [];
        buffers_objeto = Operacao.listar();
        for operacao in buffers_objeto:
            buffers_json.append( operacao.toJson() );
        return buffers_json;
    def salvar(self):
        return False;

#            {"nome" : "operacao_status", "fields" : ["id", "nome"]},
#            {"nome" : "operacao_nivel", "fields" : ["id_operacao","id_nivel"]},
#            {"nome" : "operacao_atividade", "fields" : ["id_atividade", "id_operacao"]},