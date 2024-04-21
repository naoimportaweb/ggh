import uuid, time;

# cliente

class ForumComando:    
    def listar_topicos(self, cliente, grupo, mensagem):
        return mensagem.toJson()["listar_topicos"];
    def criar_topico(self, cliente, grupo, mensagem):
        return mensagem.toJson()["forum"];
    def listar_threads(self, cliente, grupo, mensagem):
        return mensagem.toJson()["listar_threads"];
    def criar_thread(self, cliente, grupo, mensagem):
        return mensagem.toJson()["forum"];
    def listar_respostas(self, cliente, grupo, mensagem):
        return mensagem.toJson()["forum_resposta"];
    def criar_resposta(self, cliente, grupo, mensagem):
        return mensagem.toJson()["forum"];