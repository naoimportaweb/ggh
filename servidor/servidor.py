#!/usr/bin/python3
import asyncio, logging, json, os, sys, inspect;
import  base64, uuid
import importlib
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
from comandos import *

TAMANHO = 16

class ServidorGrupo(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password);
        self.grupo = Grupo( jid );
        self.clientes = {};
        # Primeiro deve-se registrar os eventos XMPP, o evento será processado pelo método definido aqui
        self.add_event_handler("session_start", self.session_start);
        self.add_event_handler("message", self.message);
        
 
    def session_start(self, event):
        self.send_presence();
        self.get_roster();
        print("Done");
 
    def message(self, msg):
        #print( dir( msg['from'] )  )
        #print('bare', msg['from'].bare, '; domain', msg['from'].domain, '; full', msg['from'].full, '; host', msg['from'].host, '; jid', msg['from'].jid, '; local',
        #msg['from'].local, '; node', msg['from'].node, '; resource', msg['from'].resource, '; server', msg['from'].server, '; unescape', msg['from'].unescape, '; user', msg['from'].user, '; username', msg['from'].username);
        #bare hacker.cliente.1@xmpp.jp ; domain xmpp.jp ; full hacker.cliente.1@xmpp.jp/836571472410685651457662818 ; host xmpp.jp ; jid hacker.cliente.1@xmpp.jp/836571472410685651457662818 ; local hacker.cliente.1 ; node hacker.cliente.1 ; resource 836571472410685651457662818 ; server xmpp.jp ; unescape <bound method JID.unescape of hacker.cliente.1@xmpp.jp/836571472410685651457662818> ; user hacker.cliente.1 ; username hacker.cliente.1
        nick = msg['from'].bare;
        if self.clientes.get( nick ) == None:
            self.clientes[ nick ] = Cliente( nick, self.grupo );
        if msg['type'] in ('chat', 'normal'):
            message = Mensagem( self.clientes[ nick ], msg['from'], self.grupo.jid );
            message.fromString( msg['body'] );
            js = message.toJson();
            MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"])
            instance = MyClass()
            retorno_metodo = getattr(instance, js["funcao"])( self.clientes[ nick ], self.grupo, message );
            comando_retorno = Comando(js["modulo"], js["comando"], js["funcao"], retorno_metodo );
            mensagem_retorno = Mensagem( self.clientes[ nick ], self.clientes[ nick ].jid, self.grupo.jid);
            msg.reply( mensagem_retorno.criar( comando_retorno, criptografia="&1&" ) ).send();

 
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
    xmpp.connect();
    xmpp.process();
