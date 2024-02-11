import json;

class Conhecimento:
    def __init__(self):
        self.id = None;
        self.id_cliente = None;
        self.id_revisor = None;
        self.id_nivel = None;
        self.id_grupo = None;
        self.titulo = None;
        self.tags = None;
        self.descricao = None;
        self.texto = None;
        self.status = 0;
    
    def fromJson(self, js ):
        self.id = js["id"];
        self.id_cliente = js["id_cliente"];
        self.id_revisor = js["id_revisor"];
        self.id_nivel = js["id_nivel"];
        self.id_grupo = js["id_grupo"];
        self.titulo = js["titulo"];
        self.tags = js["tags"];
        self.descricao = js["descricao"];
        self.texto = js["texto"];
        self.status = js["status"];
    
    def toJson(self):
        return {"id" : self.id, "id_cliente" : self.id_cliente, "id_revisor" : self.id_revisor, "id_nivel" : self.id_nivel, "id_grupo" : self.id_grupo, "titulo" : self.titulo, "tags" : self.tags, "descricao" : self.descricao, "texto" : self.texto, "status" : self.status};

