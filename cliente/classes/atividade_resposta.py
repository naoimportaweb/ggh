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
    
    def toJson(self):
        return {"id" : self.id, "id_atividade" : self.id_atividade, "id_cliente" : self.id_cliente, "id_avaliador" : self.id_avaliador,
                 "data" : self.data, "pontos" : self.pontos, "data_avaliador" : self.data_avaliador, "consideracao_avaliador" : self.consideracao_avaliador,
                 "resposta" : self.resposta};    