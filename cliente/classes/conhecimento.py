import json, re, base64, requests;

from api.fsseguro import FsSeguro;

def hexuuid():
    return uuid.uuid4().hex
def splitext(p):
    return os.path.splitext(p)[1].lower()
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

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
        self.id_status = 0;
        self.nome_status = "";
        self.comentario = "";
    
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
        self.id_status = js["id_status"];
        if js.get("nome_status") != None:
            self.nome_status = js["nome_status"];
        if js.get("comentario") != None:
            self.comentario = js["comentario"];
    
    def toJson(self):
        return {"id" : self.id, "id_cliente" : self.id_cliente, "id_revisor" : self.id_revisor, "id_nivel" : self.id_nivel, "id_grupo" : self.id_grupo, "titulo" : self.titulo, "tags" : self.tags, "descricao" : self.descricao, "texto" : self.texto, "id_status" : self.id_status, "comentario" : self.comentario};

    def setHtml(self, html):
        self.texto = html;

    def salvar(self, chave, path):
        fs = FsSeguro(chave);
        fs.escrever_json( path + "/" + self.id, self.toJson() );

    def carregar(self, chave, path):
        fs = FsSeguro(chave);
        self.fromJson( fs.ler_json( path ) );

    def substituir_url_imagem(self, html, url):
        conteudo_base = base64.b64encode(requests.get(url).content);
        return html.replace( url, "data:image/*;base64," + conteudo_base.decode("utf-8")) ;
    def substituir_url_link(self, html, url):
        partes = re.findall(r'href=[\'|\"](.*?)[\'|\"]', url[0]  );
        if len(partes) > 0:
            html = html.replace('<a'+ url[0] +'>'+ url[1] +'</a>',  striphtml( url[1] ) + " (" + partes[0] + ")" );
        else:
            html = html.replace('<a'+ url[0] +'>'+ url[1] +'</a>', "" );
        return html;
    
    def limpar_tags_indesejadas(self, html):
      scripts = re.compile(r'<(script).*?</\1>(?s)')
      css = re.compile(r'<style.*?/style>')
      a = re.compile(r'<a.*?/a>')
      html = scripts.sub('', html)
      html = css.sub('', html)
      html = a.sub('', html)
      return html;