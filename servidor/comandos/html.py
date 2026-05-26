import uuid;

# servidor
from classes.mysqlhelp import MysqlHelp

class HtmlComando:
    def get(self, cliente, grupo, mensagem):
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "SELECT * FROM `html` where id = %s  ";
        lista = my.datatable(sql, [ js["path"] ] );
        if len(lista) > 0:
            return {"html" : lista[0]["html"], "path" : js["path"] };
        else:
            return {"html" : "", "path" : js["path"] };

    def post(self, cliente, grupo, mensagem):
        #TODO: validar permissao: recomendacao_editar
        my = MysqlHelp();
        js = mensagem.toJson();
        sql = "UPDATE `html` SET `html`.html=%s where id = %s  ";
        my.execute(sql, [js["html"], js["path"] ] );
        sql = "SELECT * FROM `html` where id = %s  ";
        lista = my.datatable(sql, [ js["path"] ] );
        return {"html" : lista[0]["html"], "path" : js["path"] };
