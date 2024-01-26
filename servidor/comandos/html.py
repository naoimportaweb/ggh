import uuid;

# servidor

class Html:	
	def get(self, cliente, grupo, mensagem):
		js = mensagem.toJson();
		return {"html" : "<html>Um html idiota.</html>", "path" : js["path"] };
