import uuid;

# servidor

class ClienteCadastro:    
    def cadastro(self, cliente, grupo, mensagem):
        retornar = { "apelido" : cliente.apelido, "nivel_posicao" : cliente.nivel_posicao, "id_nivel" : cliente.id_nivel };
        return retornar;
