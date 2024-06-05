import uuid, os, sys, hashlib, json;
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from api.fsseguro import FsSeguro;
from classes.singleton.configuracao import Configuracao;

def criar_diretorio_se_nao_existe(diretorio):
    if not os.path.exists( diretorio ):
        os.makedirs( diretorio );

class Cliente:
    def __init__(self, jid,  grupo, chave_local):
        if type(jid) != type(""):
            raise Exception("JID do cliente tem que ser uma STRING.")
        self.id = hashlib.md5( jid.encode() ).hexdigest(); #str(jid).replace("/","-");
        self.jid = jid;
        self.public_key = None;
        self.private_key = None;
        self.password = None;
        self.identificacao_unica_servidor = None;
        self.chave_servidor = None;
        self.grupo = grupo;
        self.key_pair = None;
        self.chave_local = chave_local;
        self.nivel_posicao = 0;
        self.apelido = "";
        self.id_nivel = None;
        self.tags = None;
        self.pontuacao_data_processamento = None;
        self.fs = FsSeguro( chave_local );
        self.configuracao = None;
        
        self.path_cliente = self.grupo.path_grupo + "/clientes/" + hashlib.md5( jid.encode("utf-8") ).hexdigest();
        if not os.path.exists( self.path_cliente ):
            os.makedirs( self.path_cliente );
        self.configuracao = Configuracao( self.path_cliente, self.fs );

        self.path_public_key = self.path_cliente + "/public_key.txt";
        self.path_private_key = self.path_cliente + "/private_key.txt";
        self.path_mensagens = self.path_cliente + "/mensagens";
        self.path_conhecimento = self.path_cliente + "/conhecimento";
        self.path_atividade = self.path_cliente + "/atividade";
        criar_diretorio_se_nao_existe(self.path_mensagens);
        criar_diretorio_se_nao_existe(self.path_conhecimento);
        criar_diretorio_se_nao_existe(self.path_atividade);
        
        if not os.path.exists( self.path_private_key ):
            print("\033[91mATENÇÃO:\033[0m\033[96mNão existe o caminho: "+ self.path_private_key +"\033[0m");
            self.criar_chaves();
        self.private_key = RSA.importKey( self.fs.ler_binario( self.path_private_key ) );
        self.public_key = self.fs.ler_binario(self.path_public_key).decode("utf-8");
    
    def toJson(self):
        with open( self.path_private_key , "rb") as f:
            encoded_private_key = base64.b64encode(f.read()).decode("utf-8");
        with open( self.path_public_key ,  "rb") as f:
            encoded_public_key = base64.b64encode(f.read()).decode("utf-8");
        return {"jid" : self.jid, "public_key" : encoded_public_key, "password" : self.password, "private_key" : encoded_private_key, 
            "jid_grupo" : self.grupo.jid, "identificacao_unica_servidor" : self.identificacao_unica_servidor };
    def posso_tag(self, sigla):
        if self.tags == None:
            return False;
        for tag in self.tags:
            
            if tag["sigla"] == sigla:
                return True;
        return False;

    def chave_publica(self):
        self.private_key = RSA.importKey( self.fs.ler_binario( self.path_private_key ) );
        self.public_key = self.fs.ler_binario(self.path_public_key).decode("utf-8");
        return self.public_key ;

    def chave_publica_salvar(self, chave):
        self.fs.escrever_binario(self.path_public_key , chave.encode("utf-8") );

    def criar_chaves(self):
        if os.path.exists( self.path_private_key ):
            return;
        print("\033[91mATENÇÃO:\033[0m\033[96mChave sendo redefinida\033[0m");
        self.key_pair = RSA.generate(3072);
        public_key = self.key_pair.publickey();
        pubKeyPEM = public_key.exportKey();
        self.private_key = self.key_pair.exportKey();
        self.public_key = public_key.exportKey().decode("utf-8");
        self.fs.escrever_binario(self.path_private_key, self.private_key );
        self.fs.escrever_binario(self.path_public_key , self.public_key.encode("utf-8") );

