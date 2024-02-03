import sys, os, hashlib;

def criar_diretorio_se_nao_existe(diretorio):
    if not os.path.exists( diretorio ):
        os.makedirs( diretorio );
class Grupo:
    def __init__(self, jid_grupo):
        # iniciar diretórios
        self.jid = jid_grupo;
        self.niveis = [];
        self.tags = [];
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
        chave_simetrica =  str( uuid.uuid5(uuid.NAMESPACE_URL, semente + cliente ) )[0:16];
        self.clientes[ cliente ] = chave_simetrica; 
        return chave_simetrica;
        