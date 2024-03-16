import uuid;

# no cliente

class ClienteCadastroComando:    
    def cadastro(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.apelido =       js["apelido"];
        cliente.nivel_posicao = js["nivel_posicao"];
        cliente.tags =          js["tags"];
        print(cliente.tags);
        return { "apelido" : cliente.apelido };
