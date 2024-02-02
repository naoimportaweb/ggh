import uuid, time;

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
        #https://stackoverflow.com/questions/60884078/use-a-list-in-prepared-statement
        sql_clientes = "select distinct cl.id as id, cl.apelido as apelido, cl.public_key as public_key, nicl.id_nivel as nivel from cliente as cl inner join nivel_cliente as nicl on cl.id = nicl.id_cliente where nicl.id_nivel in ('3', '4')";
        buffer = ();
        lista = list(buffer);
        for nivel in js['niveis']:
            lista.append(nivel);
        lista_clientes = my.datatable(sql_clientes, []);
        return {"clientes" : lista_clientes };

    def enviar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql_cliente = "select cl.id, ni.posicao from cliente as cl inner join nivel_cliente as nicl on cl.id = nicl.id_cliente inner join nivel as ni on nicl.id_nivel = ni.id where cl.apelido = %s";
        sql_niveis = "select * from nivel as ni where ni.posicao <= (select posicao from nivel where id = %s )";
        cliente_remetente =    my.datatable( sql_cliente, [ js["apelido_remetente"] ] )[0];
        cliente_destinatario = my.datatable( sql_cliente, [ js["apelido_destinatario"] ] )[0];
        niveis = my.datatable( sql_niveis, [ js["nivel"] ] );
        
        id_mensagem = my.chave_string("mensagem", "id", 20 );
        sql_insercao_mensagem = "INSERT INTO mensagem(id, ordem, id_remetente, id_destinatario, mensagem_criptografada, chave_simetrica_criptografada, data_hora_envio) values(%s, %s, %s, %s, %s, %s, %s)";
        sql_insercao_mensagem_velues = [ id_mensagem, str(time.time()) , cliente_remetente["id"], cliente_destinatario["id"], js["mensagem_criptografada"], js["chave_simetrica_criptografada" ], datetime.now().strftime('%Y-%m-%d %H:%M:%S') ];
        
        sqls = [sql_insercao_mensagem];
        valuess = [sql_insercao_mensagem_velues];
        for nivel in niveis:
            if int(cliente_remetente["posicao"]) >= int(nivel["posicao"]) and int(cliente_destinatario["posicao"]) >= int(nivel["posicao"]):
                sql_insercao_mensagem_nivel = "INSERT INTO mensagem_nivel(id_nivel, id_mensagem) values (%s, %s)";
                sql_insercao_mensagem_nivel_values = [ nivel['id'] , id_mensagem];
                sqls.append(sql_insercao_mensagem_nivel);
                valuess.append(sql_insercao_mensagem_nivel_values);
        my.executes(sqls, valuess);
        return {"resultado" :  True };

    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select mess.id as id, mess.ordem as ordem, mess.id_remetente as id_remetente, mess.id_destinatario as id_destinatario, mess.mensagem_criptografada as mensagem_criptografada, mess.chave_simetrica_criptografada as chave_simetrica_criptografada,  TO_CHAR(mess.data_hora_envio, 'YY-MM-DD HH24:MI:SS') as  data_hora_envio, messn.id_nivel as id_nivel from mensagem as mess inner join mensagem_nivel as messn on mess.id = messn.id_mensagem where mess.id_destinatario = %s and messn.id_nivel = %s"
        return { "retorno" :  my.datatable(sql, [ cliente.id, js["id_nivel"] ] ) };

    def delete(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        if len( my.datatable("select * from mensagem where id = %s and id_destinatario = %s", [ js["id_mensagem"], cliente.id ])) > 0:
            sql_nivel_excluir = "delete from mensagem_nivel where id_mensagem = %s";
            sql_mensagem_excluir = "delete from mensagem where id = %s";
            sqlss = [sql_nivel_excluir, sql_mensagem_excluir];
            valuess = [ [js["id_mensagem"]], [js["id_mensagem"]] ];
            return { "retorno" : my.executes( sqlss, valuess ) };
        return False;
