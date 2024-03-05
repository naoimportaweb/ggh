import uuid, time;

 # servidor
from classes.mysqlhelp import MysqlHelp

# STATUS:
# 0 - Ediçao;
# 1 - Aguardando aprovação
# 2 - Aprovado

class ConhecimentoComando:
    def novo(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_nivel( js["id_nivel"] ):
        	return {"status" : False };
        sql = "INSERT INTO conhecimento (id, id_cliente, id_nivel, id_grupo, titulo, tags, descricao, texto, status, id_revisor, ultima_alteracao ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
        js["id"] = my.chave_string("conhecimento", "id", 30 );
        js["id_cliente"] = cliente.id;
        js["id_grupo"] = grupo.id;
        js["status"] = 0;
        values = [ js["id"], js["id_cliente"], js["id_nivel"], js["id_grupo"], js["titulo"], js["tags"], js["descricao"], js["texto"], js["status"], None, time.time() ];
        my.execute(sql, values);
        return {"status" : True, "conhecimento" : js };
    
    def carregar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT * FROM conhecimento where id = %s";
        values = [ js["id"] ];
        conhecimento = my.datatable(sql, values)[0];
        if not cliente.posso_nivel( conhecimento["id_nivel"] ):
            return {"status" : False, "erro" : "Não tem permissão para ver este nível."};
        return {"status" : True, "conhecimento" : conhecimento };
    
    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_nivel( js["id_nivel"] ):
            return {"lista" : [] };
        sql = "select co.* from conhecimento as co inner join cliente as cl on co.id_cliente = cl.id where ( co.id_cliente <> %s and co.id_nivel= %s and co.status <> 0 ) or (co.id_cliente = %s and co.id_nivel= %s)";
        values = [ cliente.id, js["id_nivel"], cliente.id, js["id_nivel"] ];
        return {"lista" : my.datatable(sql, values) };
    
    def aprovar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT * FROM conhecimento where id = %s";
        values = [ js["id"] ];
        conhecimento = my.datatable(sql, values)[0];
        if conhecimento["status"] != 1:
            return {"status" : False, "erro" : "Não está aguardando aprovação"};
        #sql = "SELECT tg.* FROM tag  as tg inner join tag_cliente as tgc on tg.id = tgc.id_tag where tg.sigla = 'aprovador_conhecimento' and tgc.id_cliente =  %s";
        #values = [ cliente.id ];
        #tag = my.datatable(sql, values);
        #if len(tag) == 0:
        #    return {"status" : False, "erro" : "Não tem permissão para aprovar."};
        if not cliente.posso_tag("aprovador_conhecimento"):
            return {"status" : False, "erro" : "Não tem permissão para aprovar."};
        sql = "UPDATE conhecimento set ultima_alteracao = %s, status = %s where id = %s";
        values = [ time.time(), 2, js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "conhecimento" : js };
    
    def salvar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT * FROM conhecimento where id = %s";
        values = [ js["id"] ];
        conhecimento = my.datatable(sql, values)[0];
        if conhecimento["id_cliente"] != cliente.id or conhecimento["status"] != 0:
            return {"status" : False, "erro" : "Tem que ser do autor e estar em edição."};
        sql = "UPDATE conhecimento set ultima_alteracao = %s, id_nivel = %s, titulo = %s, tags = %s, descricao = %s, texto = %s where id = %s";
        values = [ time.time(), js["id_nivel"],             js["titulo"], js["tags"], js["descricao"], js["texto"], js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "conhecimento" : js };
