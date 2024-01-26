import uuid;

from api.fsseguro import FsSeguro;

# no cliente

class Html:
    def get(self, cliente, grupo, mensagem):
        fs = FsSeguro( cliente.chave_servidor );
        js = mensagem.toJson();
        fs.escrever_raw( grupo.path_grupo_html + "/" + js["path"], js["html"]);
        return js["path"];
