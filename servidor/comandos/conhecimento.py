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
        #TODO: validar permissao: aprovador_conhecimento
        if not cliente.posso_nivel( js["id_nivel"] ):
            return {"status" : False };
        sql = "INSERT INTO conhecimento (id, id_cliente, id_nivel, id_grupo, titulo, tags, descricao, texto, id_status, id_revisor, ultima_alteracao ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
        js["id"] = my.chave_string("conhecimento", "id", 30 );
        js["id_cliente"] = cliente.id;
        js["id_grupo"] = grupo.id;
        js["id_status"] = 0;
        values = [ js["id"], js["id_cliente"], js["id_nivel"], js["id_grupo"], js["titulo"], js["tags"], js["descricao"], js["texto"], js["id_status"], None, time.time() ];
        my.execute(sql, values);
        return {"status" : True, "conhecimento" : js };
    
    def carregar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT co.*, cos.nome as nome_status  FROM conhecimento as co  inner join conhecimento_status as cos on co.id_status = cos.id where co.id = %s";
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
        sql = "select * from nivel where id=%s";
        nivel = my.datatable(sql, [js["id_nivel"]])[0];
        sql = "select co.*, cos.nome as nome_status from conhecimento as co inner join cliente as cl on co.id_cliente = cl.id inner join conhecimento_status as cos on co.id_status = cos.id where ( co.id_cliente <> %s and co.id_nivel in (select id from nivel where posicao <= %s) and co.id_status <> 0 ) or (co.id_cliente = %s)";
        values = [ cliente.id, nivel["posicao"] , cliente.id ];
        return {"lista" : my.datatable(sql, values) };
    
    def salvar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT * FROM conhecimento where id = %s";
        values = [ js["id"] ];
        conhecimento = my.datatable(sql, values)[0];
        if conhecimento["id_cliente"] != cliente.id or conhecimento["id_status"] != 0:
            return {"status" : False, "erro" : "Tem que ser do autor e estar em edição."};
        sql = "UPDATE conhecimento set ultima_alteracao = %s, id_nivel = %s, titulo = %s, tags = %s, descricao = %s, texto = %s where id = %s";
        values = [ time.time(), js["id_nivel"],             js["titulo"], js["tags"], js["descricao"], js["texto"], js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "conhecimento" : js };
    def alterar_status(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("aprovador_conhecimento"):
            return {"status" : False, "erro" : "Não tem permissão para aprovar."};
        sql = "UPDATE conhecimento set ultima_alteracao = %s, id_status = %s, pontuacao=%s where id = %s";
        values = [ time.time(), js["id_status"], js["pontuacao"], js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "conhecimento" : js };