import uuid, os, sys, hashlib, json, time, traceback;

class Operacao():
    def __init__(self):
        self.id = None ;
        self.nome = None;
        self.sigla = None;
        self.id_grupo = None;
        self.id_operacao_status = None;
        self.data_inicio = None;
        self.data_fim = None;
        self.missao = None;
        self.foco = None;
        self.operacao_status = None;
        self.id_nivel = None;
        self.atividades = [];
        self.nome_nivel = "";
    def fromJson(self, js):
        self.id = js["id"];
        self.nome = js["nome"];
        self.sigla = js["sigla"];
        self.id_nivel = js["id_nivel"];
        self.id_grupo = js["id_grupo"];
        self.id_operacao_status = js["id_operacao_status"];
        self.data_inicio = js["data_inicio"];
        self.data_fim = js["data_fim"];
        self.missao = js["missao"];
        self.foco = js["foco"];
        self.nome_nivel = js["nome_nivel"];
        if js.get("atividades") != None:
            self.atividades = js["atividades"];
        return True;
    def toJson(self):
    	return {"id" : self.id, "id_nivel" : self.id_nivel ,"sigla" : self.sigla, "nome" : self.nome, "id_grupo" : self.id_grupo, "id_operacao_status" : self.id_operacao_status, "data_inicio" : self.data_inicio, "data_fim" : self.data_fim, "missao" : self.missao, "foco" : self.foco}

    