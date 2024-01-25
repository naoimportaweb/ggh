import uuid;

class Html:
	def retorno(self, cliente, mensagem):
		js = mensagem.toJson();
		return {"html" : js["html"], "path" : js["path"] };
