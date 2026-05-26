import json, hashlib, time;

from datetime import datetime

class AtividadeResposta:
    def __init__(self):
        self.id = hashlib.md5( str(time.time()).encode() ).hexdigest();
        self.id_atividade = None;
        self.id_cliente = None;
        self.id_avaliador = None;
        self.data = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
        self.pontos = None;
        self.data_avaliador = None;
        self.consideracao_avaliador = None;
        self.resposta = None;
        self.id_status = 0;
        self.chave_publica = None;

    def fromJson(self, js):
        self.id = js["id"];
        self.id_atividade = js["id_atividade"];
        self.id_cliente = js["id_cliente"];
        self.id_avaliador = js["id_avaliador"];
        self.data = js["data"];
        self.pontos = js["pontos"];
        self.data_avaliador = js["data_avaliador"];
        self.consideracao_avaliador = js["consideracao_avaliador"];
        self.resposta = js["resposta"]; 
        if js.get("chave_publica") != None:
            self.chave_publica = js["chave_publica"];
        if js.get("id_status") != None:
            self.id_status = js["id_status"];
    
    def getStatus(self):
        if self.id_status == 0:
            return "Aguardando";
        elif self.id_status == 1:
            return "Reprovado";
        else:
            return "Aprovado"; 
    
    def getPontos(self):
        if self.pontos == None:
            return "-";
        return str(self.pontos);

    def toJson(self):
        return {"id" : self.id, "id_atividade" : self.id_atividade, "id_cliente" : self.id_cliente, "id_avaliador" : self.id_avaliador,
                 "data" : self.data, "pontos" : self.pontos, "data_avaliador" : self.data_avaliador, "consideracao_avaliador" : self.consideracao_avaliador,
                 "resposta" : self.resposta, "id_status" : self.id_status, "chave_publica" : self.chave_publica};    