import uuid, time;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime

class ForumComando:    
    def listar_topicos(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select topi.*, (select count(*) from forum_thread where id_forum_topico = topi.id) as total from forum_topico as topi where topi.id_nivel in ( select id from nivel where posicao <= %s and id_grupo=%s) order by topi.sequencia asc";
        lista = my.datatable(sql, [ cliente.nivel_posicao, grupo.id ]);
        return {"listar_topicos" : lista };

    def criar_topico(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        #if not cliente.posso_tag("forum_criar"):
        #    return {"status" : False, "erro" : "Não tem permissão para criar um item do fórum."};
        js["id"] = my.chave_string("forum_topico", "id", 30 );
        sql = "INSERT INTO forum_topico(id, id_nivel, titulo, id_grupo, descricao, sequencia) values(%s, %s, %s, %s, %s, %s)";
        data = datetime.now().isoformat();
        sequencia = datetime.now().strftime("%Y%m%d%H%M%S");
        values = [js["id"], js["id_nivel"], js["titulo"], grupo.id, js["descricao"], sequencia];
        my.execute(sql, values);
        return {"status" : True, "forum" : js };

    def listar_threads(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select * from forum_thread where id_forum_topico=%s order by data_cadastro desc";
        lista = my.datatable(sql, [ js["id_forum_topico"] ]);
        return {"listar_threads" : lista };
    def criar_thread(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        js["id"] = my.chave_string("forum_thread", "id", 30 );
        sql = "INSERT INTO forum_thread(id, id_forum_topico, titulo, id_cliente, texto, data_cadastro) values(%s, %s, %s, %s, %s, %s)";
        data = datetime.now().isoformat();
        sequencia = datetime.now().strftime("%Y%m%d%H%M%S");
        values = [js["id"], js["id_forum_topico"], js["titulo"], js["id_cliente"], js["texto"], data];
        my.execute(sql, values);
        return {"status" : True, "forum" : js };
    def listar_respostas(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select * from forum_resposta where id_forum_thread=%s";
        lista = my.datatable(sql, [ js["id_forum_thread"] ]);
        return {"forum_resposta" : lista };
    def criar_resposta(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        js["id"] = my.chave_string("forum_resposta", "id", 30 );
        sql = "INSERT INTO forum_resposta(id, id_forum_thread, id_cliente, texto, data_cadastro) values(%s, %s, %s, %s, %s)";
        data = datetime.now().isoformat();
        sequencia = datetime.now().strftime("%Y%m%d%H%M%S");
        values = [js["id"], js["id_forum_thread"], js["id_cliente"], js["texto"], data];
        my.execute(sql, values);
        return {"status" : True, "forum" : js };
