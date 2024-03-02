import json;

class Nivel:
    def __init__(self, js=None):
        self.id = "";
        self.nome = "";
        self.id_grupo = "";
        self.posicao = "";
        self.pontuacao = "";
        self.tempo = "";
        if js != None:
            self.fromJson( js );

    def fromJson(self, js):
        self.id = js["id"];
        self.nome  = js["nome"];
        self.id_grupo  = js["id_grupo"];
        self.posicao = js["posicao"];
        self.pontuacao = js["pontuacao"];
        self.tempo  = js["tempo"];

    def fromString(self, texto):
        js = json.loads( texto );
        return self.fromJson( js );
    
    def toJson(self):
        return { "id" : self.id, "nome" : self.nome, "id_grupo" : self.id_grupo, "posicao" : self.posicao, "pontuacao" : self.pontuacao, "tempo" : self.tempo };
