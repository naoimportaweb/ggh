import uuid;


# no cliente

class ChaveSimetrica:
	def gerar(self, cliente, grupo, mensagem):
		js = mensagem.toJson();
		cliente.chave_servidor = js["chave"];
		return None;
