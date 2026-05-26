import uuid, os, sys, hashlib, json, time;

class Mural:
    def __init__(self):
        self.id = None;
        self.id_grupo = None;
        self.id_cliente = None;
        self.titulo = None;
        self.mensagem = None;
        self.data = None;
        self.id_nivel = None;
        self.id_destinatario = None;
        self.sequencia = None;
    def fromJson(self, js):
        self.id = js["id"];
        self.id_grupo = js["id_grupo"];
        self.id_cliente = js["id_cliente"];
        self.titulo = js["titulo"];
        self.mensagem = js["mensagem"];
        self.data = js["data"];
        self.id_nivel = js["id_nivel"];
        self.id_destinatario = js["id_destinatario"];
        self.sequencia = js["sequencia"];
    def toJson(self):
    	return {"id" : self.id, "id_grupo" : self.id_grupo, "id_cliente" : self.id_cliente, "titulo" : self.titulo, "mensagem" : self.mensagem,
    	    "data" : self.data, "id_nivel" : self.id_nivel, "id_destinatario" : self.id_destinatario, "sequencia" : self.sequencia};

#{"nome" : "mural", "fields" : ["id", "id_grupo", "id_cliente", "titulo", "mensagem", "data", "id_nivel", "id_destinatario", "sequencia"]},