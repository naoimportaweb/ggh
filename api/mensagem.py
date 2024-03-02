import sys, os, uuid, json, base64, time;
import xmpp;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from api.chachahelp import ChaChaHelper;

# versao:
#00

#Criptografia:
#&0& = sem criptografia;
#&1& = RSA com hcava publica
#&2& = Chave simétrica chacha
#&3& = Chave simétrica AES

#Formato
#000 = raw

#parte
#0000
#total
#0000

#messageid 32
#00000000000000000000000000

class Mensagem:
    def __init__(self, cliente, jid_from, jid_to,comando=None, criptografia="&0&", callback_retorno=""):
        self.id = str( uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) ) )[:32];
        self.versao = "00";
        self.criptografia = criptografia;
        self.formato = "000";
        self.mensagem = "";
        self.jid_from = jid_from;
        self.jid_to = jid_to;
        self.cliente = cliente;
        self.comando = comando;
        self.callback_retorno = callback_retorno;
        self.MAX_SIZE_CHAT = 4000;

    def fromString(self, mensagem):
        self.versao = mensagem[0:2];
        self.criptografia = mensagem[2:5];
        self.formato = mensagem[5:8];
        parte = mensagem[8:12];
        total = mensagem[12:16];
        self.id = mensagem[16:48]
        print(self.versao, self.criptografia, self.formato, parte, total);
        if parte != total:
            with open( "/tmp/" + self.id, "a" ) as f:
                f.write( mensagem[48:] );
            return False;
        mensagem_str = "";
        if os.path.exists("/tmp/" + self.id):
            mensagem_str = open("/tmp/" + self.id, "r").read();
        mensagem_str += mensagem[48:];
        buffer_json_envelope = None;
        if self.criptografia == "&1&":
            decryptor = PKCS1_OAEP.new( self.cliente.private_key );
            decrypted = decryptor.decrypt( base64.b64decode( mensagem_str.encode() ) ).decode();
            buffer_json_envelope = json.loads( decrypted );
        elif self.criptografia == "&2&":
            aes_help = ChaChaHelper(key=self.cliente.chave_servidor );
            mensagem_descriptografada = aes_help.decrypt( mensagem_str );
            buffer_json_envelope = json.loads( mensagem_descriptografada.encode().decode() );
        else:
            buffer_json_envelope = json.loads(mensagem_str.strip());
        self.mensagem = buffer_json_envelope["body"];
        self.id = buffer_json_envelope["head"]["id"];
        self.callback_retorno = buffer_json_envelope["head"]["callback"];
        return True;
    
    def criar(self, comando=None, versao=None, criptografia=None, formato=None ):
        if versao != None:
            self.versao = versao;
        if criptografia != None:
            self.criptografia = criptografia;
        if formato != None:
            self.formato = formato;
        if comando != None:
            self.comando = comando;
        return self.toString(self.comando);
    
    def toRaw(self):
        return json.dumps(self.mensagem);
    
    def toJson(self):
        return self.mensagem;
    
    def cabecalho(self, index, total):
        retornar = self.versao;
        retornar += self.criptografia;
        retornar += self.formato;
        retornar += str(index).rjust(4, '0');
        retornar += str(total).rjust(4, '0');
        retornar += self.id;
        return retornar;

    def enviar(self, connection):
        body = self.toString();
        if len(body) > self.MAX_SIZE_CHAT:
            partes = int(len(body)/self.MAX_SIZE_CHAT);
            if partes + self.MAX_SIZE_CHAT < len(body):
                partes += 1;
            for i in range( partes  + 1 ):
                msg_xmpp = xmpp.Message( to=self.jid_to, body= self.cabecalho( i, partes ) +  body[ i * self.MAX_SIZE_CHAT: (i + 1) * self.MAX_SIZE_CHAT  ] );
                msg_xmpp.setAttr('type', 'chat');
                connection.send( msg_xmpp );
        else:
            msg_xmpp = xmpp.Message( to=self.jid_to, body= self.cabecalho( 0, 0 ) + body );
            msg_xmpp.setAttr('type', 'chat');
            connection.send( msg_xmpp );

    def toString(self, comando=None ):
        retornar = "";
        if comando != None:
            self.comando = comando;
        enviar_envelope_json = json.dumps({"head" : {"id" : self.id, "callback" : self.callback_retorno }, "body" : json.loads(self.comando.mensagem()), "aleatoriedade" : str( uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) ) ) } );
        if self.criptografia == "&1&":
            key_pub = RSA.importKey( self.cliente.public_key );
            encryptor = PKCS1_OAEP.new( key_pub );
            encrypted = base64.b64encode( encryptor.encrypt( enviar_envelope_json.encode()  ));
            retornar += encrypted.decode("ascii");
        elif self.criptografia == "&2&":
            aes_help = ChaChaHelper(key=self.cliente.chave_servidor );
            encrypted = aes_help.encrypt( enviar_envelope_json ).decode();
            retornar += encrypted;
        else:
            retornar += enviar_envelope_json;
        return retornar;