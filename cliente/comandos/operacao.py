import uuid, time;

# cliente

class OperacaoComando:    
    def listar(self, cliente, grupo, mensagem):
        return mensagem.toJson();