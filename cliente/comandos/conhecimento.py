import uuid;

# no cliente
from classes.conhecimento import Conhecimento;
from form.form_edit_conhecimento import FormEditarConhecimento;

class ConhecimentoComando:
    def novo(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js["status"] == True:
            return js["conhecimento"];
        print( js["erro"] );
        return None;
    def carregar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js["status"] == True:
            return js["conhecimento"];
        
        print( js["erro"] );
        return None;
    def listar(self, cliente, grupo, mensagem):
        return mensagem.toJson()["lista"];
    def aprovar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];
    def salvar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];