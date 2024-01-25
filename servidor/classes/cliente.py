import uuid, os, sys, hashlib, json;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class Cliente:
    def __init__(self, jid, grupo, public_key=None):
        #jsonstr1 = json.dumps(jid.__dict__) ;
        #print("EU: ", jsonstr1);
        if type(jid) != type(""):
            raise Exception("JID do cliente tem que ser uma STRING.")
        self.id = str(jid).replace("/","-");
        self.jid = jid;
        self.public_key = public_key;
        self.chave_servidor = None;
        self.grupo = grupo;
        
        path_cliente = self.grupo.path_grupo + "/clientes/" + hashlib.md5( jid.encode() ).hexdigest();
        if not os.path.exists( path_cliente ):
            os.makedirs( path_cliente );
        
        self.path_public_key = path_cliente + "/public_key.txt";        
        if self.public_key != None:
            with open(self.path_public_key, "w") as fb:
                fb.write(self.public_key);
        if os.path.exists( self.path_public_key ):
            self.public_key = open( self.path_public_key, "r").read();
    
    def chave_publica(self):
    	if not os.path.exists( self.path_public_key ):
    		self.criar_chaves();
    	return self.public_key;

    def chave_publica_salvar(self, chave):
        self.public_key = chave;
        with open( self.path_public_key , "w") as fb:
            fb.write( self.public_key );

