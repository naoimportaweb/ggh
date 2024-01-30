import uuid;

# servidor

class Html:	
	def get(self, cliente, grupo, mensagem):
		js = mensagem.toJson();
		return {"html" : open( grupo.path_grupo_html + "/regras.html" , "r").read(), "path" : js["path"] };
