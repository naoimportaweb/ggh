import uuid;

# servidor

class ChaveSimetrica:
	def gerar(self, cliente, grupo, mensagem):
		js = mensagem.toJson();
		cliente.chave_publica_salvar( js["chave"] );
		return { "chave" :  cliente.chave_servidor };
