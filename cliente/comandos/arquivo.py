import uuid, time;

# cliente

class ArquivoComando:    
    def listar(self, cliente, grupo, mensagem):
        return mensagem.toJson()["listar"];
    def criar_arquivo(self, cliente, grupo, mensagem):
        return mensagem.toJson()["arquivo"];
    def remover(self, cliente, grupo, mensagem):
        return mensagem.toJson()["arquivo"];
    def aprovar(self, cliente, grupo, mensagem):
        return mensagem.toJson()["arquivo"];
