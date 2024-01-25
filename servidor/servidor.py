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

from api.grupo import Grupo;
from api.cliente import Cliente;
from api.mensagem import Mensagem
from api.aeshelp import AesHelper;
from comandos import *
from cliente.classes.conexao.comando import Comando;


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
 
    def message(self, msg):
        #cliente = self.clientes[ msg['from'] ];
        nick = msg['from'].full;
        if self.clientes.get( nick ) == None:
            self.clientes[ nick ] = Cliente( nick, self.grupo );
        if msg['type'] in ('chat', 'normal'):
            message = Mensagem( self.clientes[ nick ], msg['from'], self.grupo.jid );
            message.fromString( msg['body'] );
            js = message.toJson();
            MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"])
            instance = MyClass()

            comando_retorno = Comando(js["modulo"], js["comando"], js["funcao"], instance.execute( self.clientes[ nick ], message ) );
            mensagem_retorno = Mensagem( self.clientes[ nick ], self.clientes[ nick ].jid, self.grupo.jid);
            msg.reply( mensagem_retorno.criar( comando_retorno, criptografia="&1&" ) ).send();

 
if __name__ == '__main__': 
    #logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s');
    
    configuracao =  open( os.path.expanduser("~/contaservidor.txt") ).readlines() ;
    xmpp = ServidorGrupo( configuracao[0].strip() , configuracao[1].strip() );
    #xmpp.use_proxy = True
    #xmpp.proxy_config = {
    #    'host': "127.0.0.1",
    #    'port': 9054}
    xmpp.connect();
    xmpp.process();
