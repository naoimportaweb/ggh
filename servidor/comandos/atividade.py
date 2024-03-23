import uuid, time, datetime;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime

class AtividadeComando:    
    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select atv.* from atividade as atv where atv.id_nivel in ( select id_nivel from nivel_cliente where id_cliente = %s )";
        atividades = my.datatable(sql, [ cliente.id ] );
        for i in range(len(atividades)):
            sql = "select * from atividade_cliente where id_atividade = %s and id_cliente=%s";
            atividades[i]["respostas"] = my.datatable(sql, [ atividades[i]["id"], cliente.id ] );
        return { "lista" : atividades  };

    def criar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        #TODO: validar permissao:
        #if not cliente.posso_tag("atividade_criar"):
        #    return {"status" : False, "erro" : "Não tem permissão para criar uma atividade."};
        js["id"] = my.chave_string("atividade", "id", 30 );
        sql = "INSERT INTO atividade(id, id_cliente, id_grupo, id_nivel, titulo, atividade, execucoes, tentativas, instrucao_correcao, instrucao, pontos_maximo) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )";
        values = [js["id"], cliente.id, grupo.id, js["id_nivel"], js["titulo"], js["atividade"], js["execucoes"], js["tentativas"], js["instrucao_correcao"], js["instrucao"], js["pontos_maximo"]];
        my.execute(sql, values);
        return {"status" : True, "atividade" : js };

    def salvar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        #TODO: validar permissao:
        #if not cliente.posso_tag("atividade_criar"):
        #    return {"status" : False, "erro" : "Não tem permissão para salvar uma atividade."};
        sql = "UPDATE atividade SET titulo=%s, atividade=%s, execucoes=%s, tentativas=%s, instrucao_correcao=%s, instrucao=%s, pontos_maximo=%s, id_status=%s where id=%s";
        values = [js["titulo"], js["atividade"], js["execucoes"], js["tentativas"], js["instrucao_correcao"], js["instrucao"], js["pontos_maximo"], js["id_status"], js["id"]];
        my.execute(sql, values);
        return {"status" : True, "atividade" : js };

    def resposta_adicionar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        #TODO: validar permissao:
        #if not cliente.posso_tag("atividade_criar"):
        #    return {"status" : False, "erro" : "Não tem permissão para salvar uma atividade."};
        sql = "INSERT INTO atividade_cliente(id, id_atividade, id_cliente, resposta, data ) values(%s, %s, %s, %s, %s)";
        values = [my.chave_string("atividade_cliente", "id", 20 ), js["id_atividade"], cliente.id, js["resposta"],  datetime.now().isoformat() ];
        my.execute(sql, values);
        return {"status" : True, "resposta" : js };
    
    def resposta_salvar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT *  FROM atividade_cliente WHERE id=%s";
        resposta_banco = my.datatable(sql, [ js["id"] ])[0];
        if resposta_banco["id_cliente"] != js["id_cliente"]:
            return {"status" : False, "erro" : "A resposta não é sua para você alterar."};
        if resposta_banco["id_status"] != 0:
            return {"status" : False, "erro" : "A resposta não pode ser alterada."};
        sql = "UPDATE atividade_cliente resposta=%s, data=%s WHERE id=%s";
        values = [ js["resposta"],  datetime.now().isoformat(), js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "resposta" : js };
