#!/usr/bin/python3
import asyncio, logging, json, os, sys, inspect;
import  base64, uuid, time
import importlib
import asyncio
#binascii,

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from slixmpp import ClientXMPP;


CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);

sys.path.append(ROOT);
sys.path.append(CURRENTDIR);


from classes.grupo import Grupo;
from classes.cliente import Cliente;
from api.mensagem import Mensagem
from api.aeshelp import AesHelper;
from api.comando import Comando;
from api.rsahelp import RsaHelper
from classes.mysqlhelp import MysqlHelp
from comandos import *

TAMANHO = 16

# criando tabelas antes de iniciar o servidor
my = MysqlHelp();
print("- Testando o Banco de Dados.");
if my.teste() > 0:
    print("Você tem que corrigir os erros relacionados a falta de tabela/colunas no banco de dados.");
    sys.exit(1);
my = None;

class ServidorGrupo(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password);
        self.grupo = Grupo( jid );
        self.online = {};
        # Primeiro deve-se registrar os eventos XMPP, o evento será processado pelo método definido aqui
        self.add_event_handler("session_start", self.session_start);
        self.add_event_handler("message", self.message);
        
 
    def session_start(self, event):
        self.send_presence();
        self.get_roster()
        #self.get_roster();
        print("Done");
        #https://stackoverflow.com/questions/17791783/sleekxmpp-send-a-message-at-will-and-still-listen-for-incoming-messages
        #self.send_message(mto="hacker.cliente.1@xmpp.jp", mbody="some message 3", mtype='chat')
 
    def message(self, msg):
        #msg['from'].local, '; node', msg['from'].node, '; resource', msg['from'].resource, '; server', msg['from'].server, '; unescape', msg['from'].unescape, '; user', msg['from'].user, '; username', msg['from'].username);
        #bare hacker.cliente.1@xmpp.jp ; domain xmpp.jp ; full hacker.cliente.1@xmpp.jp/836571472410685651457662818 ; host xmpp.jp ; jid hacker.cliente.1@xmpp.jp/836571472410685651457662818 ; local hacker.cliente.1 ; node hacker.cliente.1 ; resource 836571472410685651457662818 ; server xmpp.jp ; unescape <bound method JID.unescape of hacker.cliente.1@xmpp.jp/836571472410685651457662818> ; user hacker.cliente.1 ; username hacker.cliente.1
        nick = msg['from'].bare;
        cliente = Cliente( nick, self.grupo );
        cliente.carregar();

        if self.online.get( cliente.jid ) == None:
            cliente.chave_servidor = str( uuid.uuid5(uuid.NAMESPACE_URL, "-") )[0:16];
        else:
            cliente.chave_servidor = online[ self.cliente.jid ];

        if msg['type'] in ('chat', 'normal'):
            print("|->\033[Chego:\033[0m", msg['from'] );
            print("      |");
            message = Mensagem( cliente, msg['from'], self.grupo.jid );
            message.fromString( msg['body'] );
            js = message.toJson();
            MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"])
            instance = MyClass()
            retorno_metodo = getattr(instance, js["funcao"])( cliente, self.grupo, message );
            comando_retorno = Comando(js["modulo"], js["comando"], js["funcao"], retorno_metodo );
            mensagem_retorno = Mensagem( cliente, cliente.jid, self.grupo.jid);

            # retornar parametros do header, tal como id e callback
            mensagem_retorno.id = message.id;
            mensagem_retorno.callback_retorno = message.callback_retorno;

            # isso foi gambiarra, forçando sem criptografia caso seja envio de chave pública, para depois ter a criptografia (a chave tem que ser transmitida né!!!).
            gambiarra_criptografia = "&1&";
            if js["comando"] != "ChaveSimetrica":
                gambiarra_criptografia = "&2&";
            print("      |->\033[94mRespondido:\033[0m", msg['from'] );
            msg.reply( mensagem_retorno.criar( comando_retorno, criptografia=gambiarra_criptografia ) ).send();

 
if __name__ == '__main__': 
    #logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s');
    configuracao = [];
    if os.path.exists(os.path.expanduser("~/.ggh_server_desenv.json")):
        configuracao =  open( os.path.expanduser("~/.ggh_server_desenv.json") ).readlines() ;
    else:
        configuracao.append( input("Informe o endereço XMPP do grupo: ") );
        configuracao.append( input("Informe o password: ") );

    xmpp = ServidorGrupo( configuracao[0].strip() , configuracao[1].strip() );
    #xmpp.use_proxy = True
    #xmpp.proxy_config = {
    #    'host': "127.0.0.1",
    #    'port': 9054}
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.connect();
    xmpp.process();
