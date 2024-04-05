import uuid;

# no cliente

class ClienteCadastroComando:    
    def cadastro(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.apelido =       js["apelido"];
        cliente.nivel_posicao = js["nivel_posicao"];
        cliente.tags =          js["tags"];
        cliente.pontuacao_data_processamento = js["pontuacao_data_processamento"];
        cliente.pontuacao =     js["pontuacao"];
        cliente.id_nivel =     js["id_nivel"];
        return { "apelido" : cliente.apelido };
    def alterar_nome(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.apelido =       js["apelido"];
        return {"status" : True};
    def atualizar_tags(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.tags =          js["tags"];
        return cliente.tags;
