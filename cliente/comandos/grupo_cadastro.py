import uuid;

# no cliente

class GrupoCadastro:    
    def lista_clientes(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        print( js["lista"] );
        return True;
