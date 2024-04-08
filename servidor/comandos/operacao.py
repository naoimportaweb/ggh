import uuid, time;

# servidor
from classes.mysqlhelp import MysqlHelp
from classes.operacao import Operacao;

from datetime import datetime

class OperacaoComando:    
    def listar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        my = MysqlHelp();
        sql = "select * from nivel where id=%s";
        nivel = my.datatable( sql, [ js["id_nivel"]  ])[0];
        sql = "select op.* from operacao as op where op.id_nivel in (select id from nivel where posicao <= %s )";
        dados = my.datatable(sql, [ nivel["posicao"] ]);
        return {"status" : True, "lista" : dados};
    def novo(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("operacao_criar"):
            return {"status" : False, "erro" : "Não tem permissão para criar uma operação."};
        sql = "INSERT INTO operacao (id, id_nivel, sigla, nome, id_grupo, id_operacao_status, data_inicio, data_fim, missao, foco ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        js["id"] = my.chave_string("operacao", "id", 30 );
        js["id_grupo"] = grupo.id;
        js["id_operacao_status"] = 0;
        values = [ js["id"], js["id_nivel"] , js["sigla"] , js["nome"] , js["id_grupo"] , js["id_operacao_status"] , js["data_inicio"] , js["data_fim"] , js["missao"] , js["foco"] ];
        my.execute(sql, values);
        return {"status" : True, "operacao" : js };
    def salvar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("operacao_criar"):
            return {"status" : False, "erro" : "Não tem permissão para criar uma operação."};
        sql = "UPDATE operacao SET sigla=%s, nome=%s, id_operacao_status=%s, data_inicio=%s, data_fim=%s, missao=%s, foco=%s where id=%s"
        values = [  js["sigla"] , js["nome"]  , js["id_operacao_status"] , js["data_inicio"] , js["data_fim"] , js["missao"] , js["foco"], js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "operacao" : js };