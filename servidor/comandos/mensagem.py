import uuid;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime

# Cliente executa a segunte sequencia:
#   1 - Passa um array de níveis e o servidor retorna um array para cada nível de {apelido, chavepublica} de cada cliente.
#   2 - O cliente para cada cliente destinatario, gera uma mensagem criptografada e manda para o servidor
#       2.1 - o servidor valida se o cliente remetente pode enviar mensagem para o cliente destinatário por meio de nível
#       2.2 - o servidor lança salvando na tabela

class Mensagem:    
    # retorna uma lista de clientes que podem acessar cada nível, então nível é um array de niveis
    def lista_clientes_niveis(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        retorno = {"niveis" : []};
        for nivel in js['niveis']:
            sql = "select distinct cl.apelido as apelido, cl.public_key as public_key from cliente as cl inner join nivel_cliente as nicl on cl.id = nicl.id_cliente inner join nivel as ni on nicl.id_nivel = ni.id where ni.posicao >= (select posicao from nivel where id = %s)";
            values = [ nivel ];
            retorno["niveis"].append( {"nivel" : nivel, "clientes" :  my.datatable(sql, values)} );
        return retorno;
    
    def enviar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql_cliente = "select cl.id, ni.posicao from cliente as cl inner join nivel_cliente as nicl on cl.id = nicl.id_cliente inner join nivel as ni on nicl.id_nivel = ni.id where cl.apelido = %s";
        sql_nivel = "select * from nivel where id = %s";
        cliente_remetente =    my.datatable( sql_cliente, [ js["apelido_remetente"] ] )[0];
        cliente_destinatario = my.datatable( sql_cliente, [ js["apelido_destinatario"] ] )[0];
        nivel = my.datatable( sql_nivel, [ js["id_nivel"] ] )[0];
        if int(cliente_remetente["posicao"]) >= int(nivel["posicao"]) and int(cliente_destinatario["posicao"]) >= int(nivel["posicao"]):
            id_mensagem = my.chave_string("mensagem", "id", 20 );
            sql_insercao = "INSERT INTO mensagem(id, id_remetente, id_destinatario, id_nivel, mensagem_criptografada, chave_simetrica_criptografada, data_hora_envio) values(%s, %s, %s, %s, %s, %s, %s)";
            values = [ id_mensagem, cliente_remetente["id"], cliente_destinatario["id"], nivel["id"], js["mensagem_criptografada"], js["chave_simetrica_criptografada" ], datetime.now().strftime('%Y-%m-%d %H:%M:%S') ];
            my.execute(sql_insercao, values);
            return {"resultado" :  True };
        return {"resultado" :  False };

    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select id, id_remetente, id_destinatario, id_nivel, mensagem_criptografada, chave_simetrica_criptografada,  TO_CHAR(data_hora_envio, 'YY-MM-DD HH24:MI:SS') as  data_hora_envio from mensagem where id_destinatario = %s and id_nivel = %s";
        return { "retorno" :  my.datatable(sql, [ cliente.id, js["id_nivel"] ] ) };

