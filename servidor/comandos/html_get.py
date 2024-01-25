import uuid;


class HtmlGet:	
	def execute(self, cliente, mensagem):
		js = mensagem.toJson();
		return {"html" : "<html>Um html idiota.</html>", "path" : js["path"] };
