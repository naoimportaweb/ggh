import uuid;

# no cliente

class ClienteCadastro:    
    def cadastro(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.apelido = js["apelido"];
        print( "APELIDO: ", cliente.apelido );
        return { "apelido" : cliente.apelido };
