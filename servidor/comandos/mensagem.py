import uuid, time;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime, timedelta

# Cliente executa a segunte sequencia:
#   1 - Passa um array de níveis e o servidor retorna um array para cada nível de {apelido, chavepublica} de cada cliente.
#   2 - O cliente para cada cliente destinatario, gera uma mensagem criptografada e manda para o servidor
#       2.1 - o servidor valida se o cliente remetente pode enviar mensagem para o cliente destinatário por meio de nível
#       2.2 - o servidor lança salvando na tabela

class MensagemComando:    
    # retorna uma lista de clientes que podem acessar cada nível, então nível é um array de niveis
    def lista_clientes_niveis(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        data_minima = datetime.now() - timedelta(days=2);
        sql = "select * from nivel where id= %s";
        nivel = my.datatable( sql, [js["nivel"]])[0];
        sql = "select distinct cl.id as id, cl.apelido as apelido, cl.public_key as public_key, cl.id_nivel as id_nivel from cliente as cl where cl.id_nivel in (select id from nivel where posicao >= %s) and cl.data_acesso >= %s ";
        lista_clientes = my.datatable(sql, [ nivel["posicao"], data_minima.isoformat() ]);
        return {"clientes" : lista_clientes };

    def enviar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql_cliente = "select cl.id, ni.posicao from cliente as cl inner join nivel as ni on ni.id = cl.id_nivel where cl.apelido = %s";
        sql_niveis = "select * from nivel as ni where ni.posicao <= (select posicao from nivel where id = %s )";
        #TODO: REVER LINHA ABAIXO, VEJA QUE CARREGA O CLIENTE QUE SOU EU.....
        cliente_remetente =    my.datatable( sql_cliente, [ js["apelido_remetente"] ] )[0];
        cliente_destinatario = my.datatable( sql_cliente, [ js["apelido_destinatario"] ] )[0];
        niveis = my.datatable( sql_niveis, [ js["nivel"] ] );
        id_mensagem = my.chave_string("mensagem", "id", 20 );
        sql_insercao_mensagem = "INSERT INTO mensagem(id, ordem, id_remetente, id_destinatario, mensagem_criptografada, chave_simetrica_criptografada, data_hora_envio, id_nivel) values(%s, %s, %s, %s, %s, %s, %s, %s)";
        sql_insercao_mensagem_velues = [ id_mensagem, str(time.time()) , cliente_remetente["id"], cliente_destinatario["id"], js["mensagem_criptografada"], js["chave_simetrica_criptografada"], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), js["nivel"] ];
        sqls = [sql_insercao_mensagem];
        valuess = [sql_insercao_mensagem_velues];
        my.executes(sqls, valuess);
        grupo.add_envio(cliente, "comandos.mensagem", "MensagemComando", "atualizar", data={"nivel" : js["nivel"] });
        return {"resultado" :  True };

    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT mess.*, TO_CHAR(mess.data_hora_envio, 'YY-MM-DD HH24:MI:SS') as  data_hora_envio, rem.apelido as apelido_remetente, des.apelido as apelido_destinatario FROM mensagem as mess inner join cliente as rem on mess.id_remetente = rem.id inner join cliente as des on des.id = mess.id_destinatario  where mess.id_destinatario = %s";
        buffers = my.datatable(sql, [ cliente.id ] );
        return { "retorno" : buffers  };

    def delete(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "delete from mensagem where id = %s and id_destinatario=%s";
        values =  [js["id_mensagem"], cliente.id] ;
        return { "retorno" : my.execute( sql, values ) };
