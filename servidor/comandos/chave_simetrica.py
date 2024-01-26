import uuid;

# servidor

class ChaveSimetrica:
	def gerar(self, cliente, grupo, mensagem):
		js = mensagem.toJson();
		cliente.chave_publica_salvar( js["chave"] );
		cliente.chave_servidor = str( uuid.uuid5(uuid.NAMESPACE_URL, "-") )[0:16];
		return { "chave" :  cliente.chave_servidor };
