import sys, os, hashlib, time, traceback;

from classes.mysqlhelp import MysqlHelp
from classes.cliente import Cliente;
from api.mensagem import Mensagem
from api.comando import Comando;


def criar_diretorio_se_nao_existe(diretorio):
    if not os.path.exists( diretorio ):
        os.makedirs( diretorio );

class Grupo:
    def __init__(self, jid, inicializacao):
        # iniciar diretórios
        self.inicializacao = inicializacao;
        self.jid = jid;
        self.id = None ;
        
        # os diretórios que serão criados para gestao do servidor
        self.path_home = os.path.expanduser("~/ggh_servidor/")
        self.path_grupo = self.path_home + "/" + hashlib.md5( jid.encode() ).hexdigest();
        self.path_grupo_html = self.path_grupo + "/html";
        self.path_grupo_public_key = self.path_grupo + "/public_key";
        self.path_grupo_apelidos = self.path_grupo + "/apelidos";
        criar_diretorio_se_nao_existe(self.path_home);
        criar_diretorio_se_nao_existe(self.path_grupo);
        criar_diretorio_se_nao_existe(self.path_grupo_html);
        criar_diretorio_se_nao_existe(self.path_grupo + "/clientes/" );
        os.environ['PATH_GRUPO'] = self.path_grupo;

        # Listas de acesso rápido
        self.clientes = {};
        self.lista_envio = [];

        # carregar do banco de dados
        self.carregar();
    
    def carregar(self):
        my = MysqlHelp();
        datatable = my.datatable("select * from grupo where jid = %s", [ self.jid ])[0];
        self.id = datatable["id"];
        datatable = my.datatable("select cli.* from cliente cli inner join grupo_cliente as grcli on cli.id = grcli.id_cliente where grcli.id_grupo = %s", [ self.jid ]);
        for cliente in datatable:
            cliente_buffer = Cliente( cliente["id"], self ); 
            cliente_buffer.fromJson( cliente );
            cliente_buffer.registra_entrada(); # registra que entrou
            self.clientes[ cliente["jid"] ] =  cliente_buffer;
    
    def cliente(self, jid):
        if self.clientes.get( jid ) == None:
            cliente_buffer = Cliente( jid, self );
            cliente_buffer.carregar();
            self.clientes[ jid ] = cliente_buffer;
        return self.clientes[ jid ];
    
    def logoff(self, jid):
        self.clientes.pop(jid, None);
    
    def add_envio(self, cliente, modulo, comando, funcao, data={}, retorno="", criptografia="&1&", id=None):
        comando  = Comando( modulo, comando, funcao, data );
        mensagem = Mensagem( cliente, self.jid, cliente.jid, comando=comando, criptografia=criptografia, id=id );
        self.lista_envio.append( mensagem );

    def clientes_nick(self):
        my = MysqlHelp();
        datatable = my.datatable("select cl.apelido from grupo_cliente as gc inner join cliente as cl on gc.id_cliente = cl.id where gc.id_grupo = %s", [ self.id ]);
        return { "lista" : datatable };
    
    def niveis(self):
        my = MysqlHelp();
        buffer =  my.datatable("select * from nivel as ni where ni.id_grupo = %s order by posicao asc", [ self.id ]);
        return buffer; 
    
    def tags(self):
        my = MysqlHelp();
        return my.datatable("select * from tag as ta where ta.id_grupo = %s", [ self.id ]);
    
    #def registrar_chave_publica(self, cliente, semente=""):
    #    chave_simetrica =  str( uuid.uuid5(uuid.NAMESPACE_URL, semente + cliente + str(time.time())) )[0:16];
    #    self.clientes[ cliente ] = chave_simetrica; 
    #    return chave_simetrica;
        


