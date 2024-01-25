import uuid;


class ChaveSimetrica:
	def retorno(self, cliente, mensagem):
		js = mensagem.toJson();
		cliente.chave_servidor = js["chave"];
		return None;
