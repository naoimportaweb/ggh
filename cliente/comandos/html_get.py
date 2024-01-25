import uuid;


class HtmlGet:
	def processar(self, cliente, mensagem):
		js = mensagem.toJson();
		return {"html" : js["html"], "path" : js["path"] };
