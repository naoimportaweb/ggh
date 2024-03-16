import sys, os, hashlib, time;

from classes.cliente import Cliente;
from api.mensagem import Mensagem;
from api.comando import Comando;

def criar_diretorio_se_nao_existe(diretorio):
    if not os.path.exists( diretorio ):
        os.makedirs( diretorio );
class Grupo:
    def __init__(self, jid_grupo):
        # iniciar diretórios
        self.jid = jid_grupo;
        self.niveis = [];
        self.tags = [];
        self.message_list_send = [];
        self.clientes = [];
        self.path_home = os.path.expanduser("~/ggh_cliente/")
        self.path_grupo = self.path_home + "/" + hashlib.md5( jid_grupo.encode() ).hexdigest();
        self.path_grupo_html = self.path_grupo + "/html";
        self.path_grupo_public_key = self.path_grupo + "/public_key";
        
        criar_diretorio_se_nao_existe(self.path_home);
        criar_diretorio_se_nao_existe(self.path_grupo);
        criar_diretorio_se_nao_existe(self.path_grupo_html);
        
        os.environ['PATH_GRUPO'] = self.path_grupo;

    def registrar_chave_publica(self, cliente, semente=""):
        chave_simetrica =  str( uuid.uuid5(uuid.NAMESPACE_URL, semente + cliente + str(time.time())) )[0:16];
        self.clientes[ cliente ] = chave_simetrica; 
        return chave_simetrica;
    
    def adicionar_mensagem(self, cliente, modulo, comando, funcao, data, criptografia="&2&", callback=None):
        comando_objeto = Comando(modulo, comando, funcao, data);
        mensagem_objeto = Mensagem( cliente, cliente.jid, self.jid, comando=comando_objeto, criptografia="&2&", callback=callback);
        self.message_list_send.append( mensagem_objeto );