import uuid, time;

from classes.atividade import Atividade;

#cliente
class AtividadeComando:    
    def listar(self, cliente, grupo, mensagem):
        lista = mensagem.toJson()["lista"];
        for elemento in lista:
            a = Atividade();
            a.fromJson( elemento );
            a.salvar( cliente.chave_local, cliente.path_atividade );
       	return True;

    def criar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];

    def salvar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        a = Atividade();
        a.fromJson( js["atividade"] );
        a.salvar( cliente.chave_local, cliente.path_atividade );
        return js["status"];

    def resposta_adicionar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];