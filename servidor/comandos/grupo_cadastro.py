import uuid;

# servidor

class GrupoCadastroComando:    
    def cadastro(self, cliente, grupo, mensagem):
        retornar = {"id" : grupo.id, "jid" : grupo.jid, "inicializacao" : grupo.inicializacao, "niveis" : grupo.niveis(), "tags" : grupo.tags(), "clientes" : self.lista_clientes(cliente, grupo, mensagem) };
        return retornar;

    def lista_clientes(self, cliente, grupo, mensagem):
        return grupo.clientes_nick();

    def participar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.chave_publica_salvar( js["chave"] );
        return { "chave" :  cliente.chave_servidor  };