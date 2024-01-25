import uuid, os, sys, hashlib, json;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from slixmpp import ClientXMPP;

class Cliente:
    def __init__(self, jid, grupo):
        #jsonstr1 = json.dumps(jid.__dict__) ;
        #print("EU: ", jsonstr1);
        if type(jid) != type(""):
            raise Exception("JID do cliente tem que ser uma STRING.")
        self.id = str(jid).replace("/","-");
        self.jid = jid;
        self.public_key = None;
        self.private_key = None;
        self.chave_servidor = None;
        self.grupo = grupo;
        self.key_pair = None;
        
        path_cliente = self.grupo.path_grupo + "/clientes/" + hashlib.md5( jid.encode() ).hexdigest();
        if not os.path.exists( path_cliente ):
            os.makedirs( path_cliente );
        self.path_public_key = path_cliente + "/public_key.txt";
        self.path_private_key = path_cliente + "/private_key.txt";
        
        if not os.path.exists( self.path_private_key ):
            self.criar_chaves();
        else:
            with open(self.path_private_key, "rb") as k:
                self.private_key = RSA.importKey( k.read() );


        #if self.public_key != None:
        #    with open(self.path_public_key, "w") as fb:
        #        fb.write(self.public_key);
        #else:
        #    if self.private_key != None:
        #        if not os.path.exists( self.path_public_key ):
        #            public_key_buffer = self.private_key.publickey();
        #            with open(self.path_public_key, "w") as fb:
        #                fb.write(public_key_buffer.exportKey().decode());
        #if os.path.exists( self.path_public_key ):
        #    self.public_key = open( self.path_public_key, "r").read();
    
    def chave_publica(self):
    	if not os.path.exists( self.path_public_key ):
    		self.criar_chaves();
    	return self.public_key;

    def chave_publica_salvar(self, chave):
        self.public_key = chave;
        with open( self.path_public_key , "w") as fb:
            fb.write( self.public_key );
            self.public_key = self.public_key.publickey();

    def criar_chaves(self):
        self.key_pair = RSA.generate(3072);
        public_key = self.key_pair.publickey();
        pubKeyPEM = public_key.exportKey();
        self.private_key = self.key_pair.exportKey();
        with open (self.path_private_key, "bw") as prv_file:
            prv_file.write( self.private_key );
        with open (self.path_public_key, "w") as pub_file:
            self.public_key = public_key.exportKey().decode();
            pub_file.write( self.public_key );
