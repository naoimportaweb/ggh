import uuid, time;

# como o retorno é uma thread e não uma QThread, dá erro no MessageBox.
#from PyQt6.QtWidgets import QMessageBox
#QMessageBox.information(self, "LISTA", "uma listagem.", QMessageBox.StandardButton.Ok);

from classes.atividade import Atividade;

#cliente
class AtividadeComando:    
    def listar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        #lista = js["lista"];
        #self.salvar_lista( cliente, lista );
       	return js;

    def criar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];

    def nao_corrigidas(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js.get("lista") != None:
            return js["lista"];
        return [];

    def salvar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        
        a = Atividade();
        a.fromJson( js["atividade"] );
        a.salvar( cliente.chave_local, cliente.path_atividade );
        return js["status"];

    def resposta_adicionar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];
    
    def resposta_salvar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js["status"] == True and js.get("lista") != None:
            lista = js["lista"];
            self.salvar_lista( cliente, lista );
        return js["status"];
    
    def resposta_aprovar_reprovar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js["status"] == True and js.get("lista") != None:
            lista = js["lista"];
            self.salvar_lista( cliente, lista );
        return js["status"];
    
    def atividade_aprovar_reprovar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js["status"] == True and js.get("lista") != None:
            lista = js["lista"];
            self.salvar_lista( cliente, lista );
        return js["status"];

    def salvar_lista(self, cliente, lista):
        for elemento in lista:
            a = Atividade();
            a.fromJson( elemento );
            a.salvar( cliente.chave_local, cliente.path_atividade );
    def associar_operacao(self, cliente, grupo, mensagem):
        return mensagem.toJson();