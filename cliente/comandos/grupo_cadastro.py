import uuid;

# no cliente

class GrupoCadastroComando:    
    def cadastro(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        grupo.niveis = js["niveis"];
        grupo.tags = js["tags"];
        grupo.clientes = js["clientes"];
        return True;
    def lista_clientes(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return True;