import uuid, time, datetime, json, os, inspect;

# servidor
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))));

class AmbienteComando:    
    def dados(self, cliente, grupo, mensagem):
    	js = json.loads( open( ROOT + "/data/versao.json" , "r").read() );
    	return {"versao" : js["versao"]};
