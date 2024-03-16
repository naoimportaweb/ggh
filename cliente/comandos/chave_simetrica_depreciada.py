import uuid;


# no cliente

class ChaveSimetricaComando:
    def gerar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.chave_servidor = js["chave"];
        return None;
    def ping(self, cliente, grupo, mensagem):
        return {"status" : True};