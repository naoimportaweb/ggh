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
        return { "apelido" : cliente.apelido };
