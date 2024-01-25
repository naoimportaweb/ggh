import sys, os, uuid, json, base64;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from api.aeshelp import AesHelper;

# versao:
#00

#Criptografia:
#&0& = sem criptografia;
#&1& = RSA com hcava publica
#&2& = Chave simétrica

#Formato
#000 = raw

class Mensagem:
    def __init__(self, cliente, jid_from, jid_to,comando=None, criptografia="&0&"):
        self.id = str( uuid.uuid5(uuid.NAMESPACE_URL, "" ) );
        self.versao = "00";
        self.criptografia = criptografia;
        self.formato = "000";
        self.mensagem = "";
        self.jid_from = jid_from;
        self.jid_to = jid_to;
        self.cliente = cliente;
        self.comando = comando;

    def fromString(self, mensagem):
        self.versao = mensagem[0:2];
        self.criptografia = mensagem[2:5];
        self.formato = mensagem[5:8];

        if self.criptografia == "&1&":
            decryptor = PKCS1_OAEP.new(self.cliente.key_pair);
            decrypted = decryptor.decrypt( base64.b64decode( mensagem[8:].encode() ) ).decode();
            self.mensagem = json.loads( decrypted );
        elif self.criptografia == "&2&":
            aes_help = AesHelper(key=self.cliente.chave_servidor );
            mensagem_descriptografada = aes_help.decrypt( mensagem[8:] );
            self.mensagem = json.loads( mensagem_descriptografada );
        else:
            self.mensagem = json.loads(mensagem[8:]);
    
    def criar(self, comando, versao=None, criptografia=None, formato=None ):
        if versao != None:
            self.versao = versao;
        if criptografia != None:
            self.criptografia = criptografia;
        if formato != None:
            self.formato = formato;
        self.comando = comando;
        return self.toString(comando);
    
    def toRaw(self):
        return json.dumps(self.mensagem);
    
    def toJson(self):
        return self.mensagem;
    
    def toString(self, comando=None ):
        retornar = self.versao;
        retornar += self.criptografia;
        retornar += self.formato;
        if comando != None:
            self.comando = comando;
        if self.criptografia == "&1&":
            key_pub = RSA.importKey( self.cliente.public_key );
            encryptor = PKCS1_OAEP.new( key_pub );
            encrypted = base64.b64encode( encryptor.encrypt( self.comando.mensagem().encode() ));
            retornar += encrypted.decode("ascii");
        elif self.criptografia == "&2&":
            aes_help = AesHelper(key=self.cliente.chave_servidor );
            encrypted = aes_help.encrypt( self.comando.mensagem() ).decode();
            retornar += encrypted;
        else:
            retornar += self.comando.mensagem();

        return retornar;