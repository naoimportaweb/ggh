import json;

class Comando:
	def __init__(self, modulo, comando, funcao, data):
		self.modulo = modulo;
		self.comando = comando;
		self.funcao = funcao;
		self.data = data;
		self.data["comando"] = self.comando;
		self.data["funcao"] = self.funcao;
		self.data["modulo"] = self.modulo;

	def mensagem(self):
		return json.dumps(self.data, default=str);

	
