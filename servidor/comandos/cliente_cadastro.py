import uuid;

# servidor

class ClienteCadastroComando:    
    def cadastro(self, cliente, grupo, mensagem):
        retornar = { "apelido" : cliente.apelido, "nivel_posicao" : cliente.nivel_posicao, "id_nivel" : cliente.id_nivel, "tags" : cliente.tags, 
            "pontuacao_data_processamento" : cliente.pontuacao_data_processamento, "pontuacao" : cliente.pontuacao };
        return retornar;
