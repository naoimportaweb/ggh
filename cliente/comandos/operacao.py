import uuid, time;

# cliente

class OperacaoComando:    
    def listar(self, cliente, grupo, mensagem):
        return mensagem.toJson();
    def novo(self, cliente, grupo, mensagem):
        return mensagem.toJson();
    def salvar(self, cliente, grupo, mensagem):
        return mensagem.toJson();