import uuid;

from api.fsseguro import FsSeguro;

# no cliente

class HtmlComando:
    def get(self, cliente, grupo, mensagem):
        fs = FsSeguro( cliente.chave_local );
        js = mensagem.toJson();
        if js["html"] != "":
            fs.escrever_raw( grupo.path_grupo_html + "/" + js["path"], js["html"]);
            return js["path"];
        else:
            return None;
    def post(self, cliente, grupo, mensagem):
        fs = FsSeguro( cliente.chave_local );
        js = mensagem.toJson();
        if js["html"] != "":
            fs.escrever_raw( grupo.path_grupo_html + "/" + js["path"], js["html"]);
            return js["path"];
        else:
            return None;