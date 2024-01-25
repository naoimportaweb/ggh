import uuid;

class ChaveSimetrica:
	def gerar(self, cliente, mensagem):
		js = mensagem.toJson();
		cliente.chave_publica_salvar( js["chave"] );
		cliente.chave_servidor = str( uuid.uuid5(uuid.NAMESPACE_URL, "-") )[0:16];
		return { "chave" :  cliente.chave_servidor };
