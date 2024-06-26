import uuid, time, datetime;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime

class AtividadeComando:    
    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select atv.*, ni.nome as nome_nivel, ni.posicao as posicao_nivel from atividade as atv inner join nivel as ni on atv.id_nivel = ni.id where ( atv.id_cliente = %s ) or ( ni.posicao <= ( select posicao from nivel where id_grupo=%s and id=%s  and atv.id_status = 2 )) order by ni.posicao ASC, ni.nome ASC";
        atividades = my.datatable(sql, [ cliente.id , grupo.id, cliente.id_nivel ] );
        for i in range(len(atividades)):
            sql = "select * from atividade_cliente where id_atividade = %s and id_cliente=%s";
            atividades[i]["respostas"] = my.datatable(sql, [ atividades[i]["id"], cliente.id ] );
            sql = "SELECT op.sigla, op.nome FROM operacao as op inner join operacao_atividade as opa on op.id = opa.id_operacao where opa.id_atividade=%s";
            atividades[i]["operacoes"] = my.datatable(sql, [ atividades[i]["id"] ] );
        return { "lista" : atividades  };

    def criar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        #TODO: validar permissao:
        if not cliente.posso_tag("atividade_criar"):
            return {"status" : False, "erro" : "Não tem permissão para criar uma atividade."};
        js["id"] = my.chave_string("atividade", "id", 30 );
        sql = "INSERT INTO atividade(id, id_cliente, id_grupo, id_nivel, titulo, atividade, execucoes, tentativas, instrucao_correcao, instrucao, pontos_maximo) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )";
        values = [js["id"], cliente.id, grupo.id, js["id_nivel"], js["titulo"], js["atividade"], js["execucoes"], js["tentativas"], js["instrucao_correcao"], js["instrucao"], js["pontos_maximo"]];
        my.execute(sql, values);
        return {"status" : True, "atividade" : self.atividade( js["id"] ) };

    def salvar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        #TODO: validar permissao:
        if not cliente.posso_tag("atividade_criar"):
            return {"status" : False, "erro" : "Não tem permissão para salvar uma atividade."};
        sql = "SELECT * FROM atividade WHERE id=%s";
        values = [js["id"]];
        resposta_banco = my.datatable(sql, values)[0];
        if resposta_banco["id_cliente"] != cliente.id:
            return {"status" : False, "erro" : "A atividade não é sua para você alterar."};
        if resposta_banco["id_status"] != 0:
            return {"status" : False, "erro" : "A atividade não pode ser salva pois está em produção ou cancelada."};
        sql = "UPDATE atividade SET id_nivel=%s, titulo=%s, atividade=%s, execucoes=%s, tentativas=%s, instrucao_correcao=%s, instrucao=%s, pontos_correcao_maximo=%s,     pontos_maximo=%s where id=%s";
        values = [js["id_nivel"], js["titulo"], js["atividade"], js["execucoes"], js["tentativas"], js["instrucao_correcao"], js["instrucao"], js["pontos_correcao_maximo"],  js["pontos_maximo"], js["id"]];
        my.execute(sql, values);
        return {"status" : True, "atividade" : js };

    def atividade_aprovar_reprovar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("atividade_criar"):
            return {"status" : False, "erro" : "Não tem permissão para salvar uma atividade."};
        
        sql = "SELECT * FROM atividade WHERE id=%s";
        values = [js["id"]];
        resposta_banco = my.datatable(sql, values)[0];
        if resposta_banco["id_cliente"] != cliente.id:
            return {"status" : False, "erro" : "A atividade não é sua para você alterar."};

        sql = "UPDATE atividade SET id_status=%s where id=%s";
        values = [ js["id_status"], js["id"]];
        my.execute(sql, values);
        return {"status" : True, "atividade" : js };

    def resposta_adicionar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        
        #sql = "SELECT atv.* FROM atividade as atv inner join atividade_cliente as atc on atv.id = atc.id_atividade WHERE atc.id=%s";
        sql = "SELECT * FROM atividade WHERE id=%s";
        values = [ js["id_atividade"] ];
        resposta_banco = my.datatable(sql, values)[0];
        if resposta_banco["id_status"] != 2:
            return {"status" : False, "erro" : "A atividade não está em uso."};

        sql = "INSERT INTO atividade_cliente(id, id_atividade, id_cliente, resposta, data, chave_publica ) values(%s, %s, %s, %s, %s, %s)";
        values = [my.chave_string("atividade_cliente", "id", 20 ), js["id_atividade"], cliente.id, js["resposta"],  datetime.now().isoformat(), my.chave_string("atividade_cliente", "chave_publica", 30 ) ];
        my.execute(sql, values);
        return {"status" : True, "resposta" : js , "lista" : self.carregar_uma_atividade(js["id"], cliente) };
    
    def resposta_salvar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT *  FROM atividade_cliente WHERE id=%s";
        resposta_banco = my.datatable(sql, [ js["id"] ])[0];
        if resposta_banco["id_cliente"] != js["id_cliente"]:
            return {"status" : False, "erro" : "A resposta não é sua para você alterar."};
        if resposta_banco["id_status"] != 0:
            return {"status" : False, "erro" : "A resposta não pode ser alterada."};
        sql = "UPDATE atividade_cliente SET resposta=%s, data=%s WHERE id=%s";
        values = [ js["resposta"],  datetime.now().isoformat(), js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "resposta" : js, "lista" : self.carregar_uma_atividade(js["id"], cliente) };

    def resposta_aprovar_reprovar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("atividade_corrigir"):
            return {"status" : False, "erro" : "Não tem permissão para aprovar ou reprovar."};
        sql = "SELECT *  FROM atividade_cliente WHERE id=%s";
        resposta_banco = my.datatable(sql, [ js["id"] ])[0];
        if resposta_banco["id_status"] != 0:
            return {"status" : False, "erro" : "A resposta não pode ser alterada."};
        sql = "UPDATE atividade_cliente SET id_avaliador=%s, id_status=%s, data_avaliador=%s, consideracao_avaliador=%s, pontos=%s WHERE id=%s";
        values = [ cliente.id, js["id_status"], datetime.now().isoformat(), js["consideracao_avaliador"], js["pontos"], js["id"] ];
        my.execute(sql, values);
        return {"status" : True, "resposta" : js, "lista" : self.carregar_uma_atividade(js["id"], cliente) };

    def carregar_uma_atividade(self, id, cliente):
        my = MysqlHelp();
        sql = "SELECT * FROM atividade WHERE id=%s";
        atividades = my.datatable(sql, [ id ] );
        for i in range(len(atividades)):
            sql = "select * from atividade_cliente where id_atividade = %s and id_cliente=%s";
            atividades[i]["respostas"] = my.datatable(sql, [ atividades[i]["id"], cliente.id ] );
        return atividades;

    def nao_corrigidas(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if not cliente.posso_tag("atividade_corrigir"):
            return {"status" : False, "erro" : "Não tem permissão para aprovar ou reprovar."};
        sql = "SELECT atc.*, atv.titulo, atv.instrucao_correcao, atv.atividade, atv.pontos_maximo FROM atividade_cliente as atc inner join atividade as atv on atc.id_atividade = atv.id WHERE atc.id_status=%s";
        resposta_banco = my.datatable(sql, [ 0 ]);
        return {"status" : True, "lista" : resposta_banco};        
    def associar_operacao(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        if not cliente.posso_tag("operacao_criar"):
            return {"status" : False, "erro" : "Não tem permissão para criar uma operação."};
        js = mensagem.toJson();
        sql = "select id, sigla, nome from operacao where sigla=%s";
        values = [js["sigla"]];
        operacao = my.datatable(sql, values)[0];

        sql = "INSERT into operacao_atividade(id_atividade, id_operacao) values (%s, %s)";
        values = [ js["id_atividade"], operacao["id"] ];
        my.execute(sql, values);
        operacao["id"] = "";
        return {"status" : True, "operacao" :  operacao };

    def atividade(self, id):
        my = MysqlHelp();
        sql = "select atv.*, ni.nome as nome_nivel, ni.posicao as posicao_nivel from atividade as atv inner join nivel as ni on atv.id_nivel = ni.id where atv.id=%s  order by ni.posicao ASC, ni.nome ASC";
        atividades = my.datatable(sql, [ id ] );
        if len(atividades) > 0:
            return atividades[0];
        return None;