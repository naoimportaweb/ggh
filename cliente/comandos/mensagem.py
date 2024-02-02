import uuid;

# cliente

# Cliente executa a segunte sequencia:
#   1 - Passa um array de níveis e o servidor retorna um array para cada nível de {apelido, chavepublica} de cada cliente.
#   2 - O cliente para cada cliente destinatario, gera uma mensagem criptografada e manda para o servidor
#       2.1 - o servidor valida se o cliente remetente pode enviar mensagem para o cliente destinatário por meio de nível
#       2.2 - o servidor lança salvando na tabela

class Mensagem:    
    # retorna uma lista de clientes que podem acessar cada nível, então nível é um array de niveis
    def lista_clientes_niveis(self, cliente, grupo, mensagem):
        # envio:  {"niveis" : ["3", "4"]}
        # recebo: {niveis : [{"nivel" : nivel, "clientes" :  { "apelido", "public_key" }}] }
        return mensagem.toJson();
    
    def enviar(self, cliente, grupo, mensagem):
        #enviar: {apelido_remetente, apelido_destinatario, id_nivel, mensagem_criptografada, chave_simetrica_criptografada  }
        #recebo: {"resultado" :  True/False };
        js = mensagem.toJson();
        return js["resultado"]; 
    
    def listar(self, cliente, grupo, mensagem):
        return mensagem.toJson();

    def delete(self, cliente, grupo, mensagem):
        return True;