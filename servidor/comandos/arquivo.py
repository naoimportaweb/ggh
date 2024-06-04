import uuid, time;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime

class ArquivoComando:    
    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select * from arquivo where id_nivel in (select id from nivel where posicao <= %s) and id_grupo=%s ";
        lista = my.datatable(sql, [ cliente.nivel_posicao, grupo.id ]);
        return {"lista" : lista };
    def criar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        js["id"] = my.chave_string("arquivo", "id", 30 );
        sql = "INSERT INTO arquivo(id, nome, descricao, urls, id_nivel, id_grupo, id_cliente, id_arquivo_tipo) values(%s, %s, %s, %s, %s, %s, %s, %s)";
        values = [js["id"], js["nome"], js["descricao"], js["urls"], js["id_nivel"], grupo.id, cliente.id, js["id_arquivo_tipo"]];
        my.execute(sql, values);
        return {"status" : True, "arquivo" : js };
    def aprovar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("arquivo_aprovar"):
            return {"status" : False };
        sql = "UPDATE arquivo set id_aprovador=%s where id=%s";
        values = [ cliente.id, js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "arquivo" : js };
    def remover(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("arquivo_aprovar"):
            return {"status" : False };
        sql = "DELETE from arquivo where id=%s";
        values = [ js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "arquivo" : js };    
