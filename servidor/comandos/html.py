import uuid;

# servidor
from classes.mysqlhelp import MysqlHelp

class HtmlComando:
    def get(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT * FROM html where nome = %s and id_grupo = %s ";
        lista = my.datatable(sql, [ js["path"], grupo.id ] );
        if lista > 0:
            return {"html" : lista[0]["html"], "path" : js["path"] };
        else:
            return {"html" : "", "path" : js["path"] };
