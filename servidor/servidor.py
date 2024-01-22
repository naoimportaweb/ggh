#!/usr/bin/python3
import asyncio, logging, json, os, sys, inspect;
import  base64, uuid
#binascii,

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from slixmpp import ClientXMPP;


CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);

sys.path.append(ROOT);
sys.path.append(CURRENTDIR);
print(sys.path);

from api.aeshelp import AesHelper;

TAMANHO = 16

class ServidorGrupo(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password);
        self.clientes = {};
        # Primeiro deve-se registrar os eventos XMPP, o evento será processado pelo método definido aqui
        self.add_event_handler("session_start", self.session_start);
        self.add_event_handler("message", self.message);
        
 
    def session_start(self, event):
        self.send_presence();
        self.get_roster();
 
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            if msg['body'].find("BEGIN PUBLIC KEY") > 0:
                key_pub = RSA.importKey( msg['body'] );
                #chave_simetrica =  "2222222222222222".encode() ;
                chave_simetrica =  str( uuid.uuid5(uuid.NAMESPACE_URL, msg['body']) )[0:16];
                self.clientes[ msg['from'] ] = chave_simetrica;  # OK, AGORA TODA COMUNICAÇÃO VAI SER CRIPTOGRAFADO COM ESSA CHAVE
                encryptor = PKCS1_OAEP.new(key_pub)
                encrypted = base64.b64encode(encryptor.encrypt( chave_simetrica.encode() ));
                msg.reply( encrypted.decode("ascii") ).send();
            else:
                # uma solicitaçao de quem já se conectou, então tenho chave simétrica.
                aes_help = AesHelper(key=self.clientes[ msg['from'] ]);
                print("Chegou criptografado: ", msg['body']);
                requisicao = aes_help.decrypt( msg['body'] );
                print("REQUISICAO:", requisicao);
                # tem que ver que tipo de comando é, trabalhar no comando, pegar o output e mandar, vou formar o retorno de um html idiota./
                msg.reply( aes_help.encrypt('{"comando" : 1, "response" : "<html>um html idooata</html>"}').decode() ).send();

        #print("[+] Mensagem enviada: ", msg['body'], "por", msg['from'], "com identificador", msg['id']);
        # agora vamos dar um retorno, afinal essa é a idéia
        #if msg['type'] in ('chat', 'normal'):
        #    msg.reply("Recebi a mensagem: " + msg['body'] + ", muito obrigado e logo entrarei em contato.").send();
 
if __name__ == '__main__': 
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s');
    
    xmpp = ServidorGrupo( "nao.importa.web@jabb3r.de" , "NTD8");
    xmpp.use_proxy = True
    xmpp.proxy_config = {
        'host': "127.0.0.1",
        'port': 9054}
    xmpp.connect();
    xmpp.process();
