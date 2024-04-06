import uuid, time;

# servidor
from classes.mysqlhelp import MysqlHelp
from classes.operacao import Operacao;

from datetime import datetime

class OperacaoComando:    
    def listar(self, cliente, grupo, mensagem):
        return {"status" : True, "operacoes" : Operacao.listar_json( cliente.nivel_posicao )};