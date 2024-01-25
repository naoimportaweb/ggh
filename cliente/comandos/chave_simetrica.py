import uuid;


class ChaveSimetrica:
	def processar(self, cliente, mensagem):
		js = mensagem.toJson();
		cliente.chave_servidor = js["chave"];
		return None;
