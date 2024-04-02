import uuid, time;

# servidor
from classes.mysqlhelp import MysqlHelp
from datetime import datetime

class MuralComando:    
    def listar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "select * from mural where id_nivel = %s or id_destinatario=%s ";
        lista = my.datatable(sql, [ cliente.id_nivel, cliente.id ]);
        return {"lista" : lista };
    def criar(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        #TODO: validar permissao:
        if not cliente.posso_tag("mural_criar"):
            return {"status" : False, "erro" : "Não tem permissão para criar um item do mural."};
        js["id"] = my.chave_string("mural", "id", 30 );
        sql = "INSERT INTO mural(id, id_grupo, id_cliente, titulo, mensagem, data, id_nivel, id_destinatario, sequencia) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)";
        data = datetime.now().isoformat();
        sequencia = datetime.now().strftime("%Y%m%d%H%M%S");
        values = [js["id"], grupo.id, cliente.id, js["titulo"], js["mensagem"], data, js["id_nivel"], js["id_destinatario"], sequencia ];
        my.execute(sql, values);
        return {"status" : True, "mural" : js };