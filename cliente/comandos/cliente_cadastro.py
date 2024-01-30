import uuid;

# no cliente

class ClienteCadastro:    
    def cadastro(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.apelido = js["apelido"];
        cliente.nivel_posicao = js["nivel_posicao"];
        return { "apelido" : cliente.apelido };
