import uuid, os, sys, hashlib, json;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import random


def gerar_palavra_aleatoria( tamanho ):
    letras = "abcdefghijklmnopqrstuvxzABCDEFGHIJKLMNOPQRSTUVXZ1234567890";
    retorno = "";
    for i in range( tamanho ):
        posicao = random.randint(0, len( letras ) );
        retorno += letras[ posicao : posicao + 1];
    return retorno;


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
        self.apelido = None;
        
        # cliente não existe, então vamos criar os diretórios dele.
        self.path_cliente = self.grupo.path_grupo + "/clientes/" + hashlib.md5( jid.encode() ).hexdigest();
        if not os.path.exists( self.path_cliente ):
            os.makedirs( self.path_cliente );
        
        self.path_cadastro = self.path_cliente + "/cadastro.json";
        if os.path.exists(self.path_cadastro):
            js_cadastro = json.loads( open( self.path_cadastro , "r" ).read() );
            self.apelido = js_cadastro["apelido"];
        else:
            self.apelido = gerar_palavra_aleatoria(8);
            with open( self.path_cadastro , "w") as f:
                f.write( json.dumps(  { "apelido" : self.apelido }  ) );
        
        self.path_public_key = self.path_cliente + "/public_key.txt";        
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

