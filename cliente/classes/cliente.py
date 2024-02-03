import uuid, os, sys, hashlib, json;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from slixmpp import ClientXMPP;

def criar_diretorio_se_nao_existe(diretorio):
    if not os.path.exists( diretorio ):
        os.makedirs( diretorio );

class Cliente:
    def __init__(self, jid,  grupo, chave_local = None):
        if type(jid) != type(""):
            raise Exception("JID do cliente tem que ser uma STRING.")
        self.id = str(jid).replace("/","-");
        self.jid = jid;
        self.public_key = None;
        self.private_key = None;
        self.chave_servidor = None;
        self.grupo = grupo;
        self.key_pair = None;
        self.chave_local = chave_local;
        self.nivel_posicao = 0;
        
        self.path_cliente = self.grupo.path_grupo + "/clientes/" + hashlib.md5( jid.encode("utf-8") ).hexdigest();
        if not os.path.exists( self.path_cliente ):
            os.makedirs( self.path_cliente );
        
        self.path_public_key = self.path_cliente + "/public_key.txt";
        self.path_private_key = self.path_cliente + "/private_key.txt";
        self.path_mensagens = self.path_cliente + "/mensagens";
        criar_diretorio_se_nao_existe(self.path_mensagens);
        
        if not os.path.exists( self.path_private_key ):
            print("\033[91mATENÇÃO:\033[0m\033[96mNão existe o caminho: "+ self.path_private_key +"\033[0m");
        self.criar_chaves();
        with open(self.path_private_key, "rb") as k:
            self.private_key = RSA.importKey( k.read() );
        with open(self.path_public_key, "rb") as k:
            self.public_key = k.read().decode("utf-8");
    
    def chave_publica(self):
        with open(self.path_private_key, "rb") as k:
            self.private_key = RSA.importKey( k.read() );
        with open(self.path_public_key, "rb") as k:
            self.public_key = k.read().decode("utf-8");
        #if not os.path.exists( self.path_public_key ):
        #    self.criar_chaves();
        return self.public_key;

    def chave_publica_salvar(self, chave):
        self.public_key = chave;
        with open( self.path_public_key , "w") as fb:
            fb.write( self.public_key );
            self.public_key = self.public_key.publickey();

    def criar_chaves(self):
        if os.path.exists( self.path_private_key ):
            return;
        print("\033[91mATENÇÃO:\033[0m\033[96mChave sendo redefinida\033[0m");
        self.key_pair = RSA.generate(3072);
        public_key = self.key_pair.publickey();
        pubKeyPEM = public_key.exportKey();
        self.private_key = self.key_pair.exportKey();
        with open (self.path_private_key, "bw") as prv_file:
            prv_file.write( self.private_key );
        with open (self.path_public_key, "wb") as pub_file:
            self.public_key = public_key.exportKey().decode("utf-8");
            pub_file.write( self.public_key.encode("utf-8") );
