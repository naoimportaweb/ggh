import uuid;

# cliente

class MuralComando:    
    # retorna uma lista de clientes que podem acessar cada nível, então nível é um array de niveis
    def listar(self, cliente, grupo, mensagem):
        return mensagem.toJson();
    def criar(self, cliente, grupo, mensagem):
        return mensagem.toJson()["status"];