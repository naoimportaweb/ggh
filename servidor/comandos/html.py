import uuid;

class Html:	
	def get(self, cliente, mensagem):
		js = mensagem.toJson();
		return {"html" : "<html>Um html idiota.</html>", "path" : js["path"] };
