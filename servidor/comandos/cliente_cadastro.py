import uuid;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime, timedelta

class ClienteCadastroComando:    
    def cadastro(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        sql = "update cliente set data_acesso = %s where id=%s";
        my.execute(sql, [datetime.now().isoformat(), cliente.id]);
        retornar = { "apelido" : cliente.apelido, "nivel_posicao" : cliente.nivel_posicao, "id_nivel" : cliente.id_nivel, "tags" : cliente.tags, 
            "pontuacao_data_processamento" : cliente.pontuacao_data_processamento, "pontuacao" : cliente.pontuacao };
        return retornar;
    def alterar_nome(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        sql = "update cliente set apelido = %s where id=%s";
        apelido = my.chave_string("cliente", "apelido", 8 );
        my.execute(sql, [apelido, cliente.id]);
        cliente.apelido = apelido;
        return {"status" : True, "apelido" : apelido};
    def atualizar_tags(self, cliente, grupo, mensagem):
        cliente.carregar_tag();
        return {"status" : True, "tags" : cliente.tags};
    def logoff(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        sql = "update cliente set chave_servidor = %s where id=%s";
        my.execute(sql, [None, cliente.id]);
        grupo.logoff( cliente.jid );
        return {"status" : True};
