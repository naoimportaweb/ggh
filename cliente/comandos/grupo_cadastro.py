import uuid;

from classes.nivel import Nivel;
from classes.tag import Tag;
# no cliente

class GrupoCadastroComando:    
    def cadastro(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        grupo.niveis = [];
        for nivel in js["niveis"]:
            grupo.niveis.append( Nivel( nivel ) );
        for tag in js["tags"]:
            grupo.tags.append( Tag( tag ) );
        grupo.id = js["id"];
        grupo.nome = js["nome"];
        grupo.descricao = js["descricao"];
        grupo.clientes = js["clientes"];
        grupo.inicializacao = js["inicializacao"];
        return True;
    
    def lista_clientes(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return True;
    def participar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        cliente.chave_servidor = js["chave"];
        return {"status" : True};
    def ping(self, cliente, grupo, mensagem):
        return {"status" : True};