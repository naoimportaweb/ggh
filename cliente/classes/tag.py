import json;

class Tag:
    def __init__( self, js=None ):
        self.id = "";
        self.nome = "";
        self.sigla = "";
        self.id_grupo = "";

    def fromJson(self,  js):
        self.id = js["id"];
        self.nome = js["nome"];
        self.sigla = js["sigla"];
        self.id_grupo = js["id_grupo"];

    def fromString(self, texto):
        return self.fromJson( json.loads( texto ) );

    def toJson(self):
        return {"id" : self.id, "nome" : self.nome, "sigla" : self.sigla, "id_grupo" : self.id_grupo };