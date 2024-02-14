#!/usr/bin/python3
import  logging, json, os, sys, inspect, base64, uuid, time, threading, importlib;
import xmpp, time, traceback, os, sys, inspect, traceback, threading, base64, importlib, uuid;

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

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

# criando tabelas antes de iniciar o servidor
my = MysqlHelp();
print("- Testando o Banco de Dados.");
if my.teste() > 0:
    print("Você tem que corrigir os erros relacionados a falta de tabela/colunas no banco de dados.");
    sys.exit(1);
my = None;


#from api.aeshelp import AesHelper;
#from classes.cliente import Cliente;
#from api.mensagem import Mensagem;
#from classes.grupo import Grupo
#from api.comando import Comando;
#   https://github.com/xmpppy/xmpppy                                                                        TEORIA
#   https://stackoverflow.com/questions/16563200/connecting-to-jabber-server-via-proxy-in-python-xmppy      PROXY

class XMPPServer:

    def __init__(self, jid_server, password):
        self.grupo = Grupo( jid_server );
        self.online = {};
        self.password = password;
        self.pausa_enviador = True; # inicamos pausados a thread, pois não estamos logados ainda.
        self.pausa_recebedor = True; # inicamos pausados a thread, pois não estamos logados ainda.
        self.connection = None;     # pipe de conexão com servidor XMPP remoto
        #self.callback = None;
        #self.chave_criptografia = chave_criptografia;
        #self.thread_enviador = None;
        #self.thread_recebedor = None;
        #self.stop_enviador = True;
        #self.stop_recebedor = True;
        #self.pausa_enviador = False;
        # TODA VEZ QUE SE GERA O OBJETO CRIA UM PAR DE CHAVE DIFERENTE;
        #           https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples
        #self.cliente = Cliente( jid_participante, self.grupo, chave_local=chave_criptografia );
        # Primeiro deve-se registrar os eventos XMPP, o evento será processado pelo método definido aqui
        #self.add_event_handler("session_start", self.session_start);
        #self.add_event_handler("message", self.message);
        #self.thread_enviador = threading.Thread(target = self.enviador, args=());
        #self.thread_enviador.start();
    def conectar(self):
        jid = xmpp.protocol.JID( self.grupo.jid );
        self.connection = xmpp.Client(server=jid.getDomain(), debug=False);
        self.connection.connect();
        if self.connection.auth(user=jid.getNode(), password=self.password, resource=jid.getResource()) != None:
            self.connection.sendInitPresence();
            self.connection.RegisterHandler('message', self.processar_mensagem);
            time.sleep(5);
            self.thread_recebedor = threading.Thread(target = self.escutar, args=());
            self.thread_recebedor.start();
            self.thread_enviador = threading.Thread(target = self.enviador, args=());
            self.thread_enviador.start();
            return True;
        return False;
    
    def enviador(self):
        while True:
            try:
                if not self.pausa_enviador and len(self.grupo.lista_envio) > 0:
                    mensagem = self.grupo.lista_envio.pop(0);
                    if mensagem != None:
                        print("Enviado:", mensagem.comando.comando);
                        print(" [+] from:", self.grupo.jid ," to:", mensagem.jid_to);
                        msg_xmpp = xmpp.Message( to=mensagem.jid_to , body=mensagem.toString() );
                        msg_xmpp.setAttr('type', 'chat');
                        self.connection.send( msg_xmpp );
                        time.sleep(0.1);
            except KeyboardInterrupt:
                sys.exit(1);
            except:
                print(".", end="");
                traceback.print_exc();
            if len(self.grupo.lista_envio) == 0 or self.pausa_enviador:
                time.sleep( 5 );
    
    def escutar(self):
        while True:
            try:
                if not self.pausa_recebedor:
                    if self.connection.Process(1) == 0:
                        time.sleep(2);
            except KeyboardInterrupt:
                sys.exit(1);
            except:
                print(".", end="");
            

    def processar_mensagem(self, conn, mess):
        try:
            text = mess.getBody();
            if text == None:
                print(mess);
                return;
            user= mess.getFrom().getNode() + "@" + mess.getFrom().getDomain();
            print("USER: ", user);
            cliente = Cliente( user, self.grupo );
            cliente.carregar();
            if self.online.get( cliente.jid ) == None:
                self.online[ cliente.jid ] = str( uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())) )[0:16];
            cliente.chave_servidor = self.online[ cliente.jid ];
            
            message = Mensagem( cliente,  user, self.grupo.jid ); # cliente, jid_from, jid_to
            message.fromString( text );
            js = message.toJson( );

            MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"])
            instance = MyClass()
            retorno_metodo = getattr(instance, js["funcao"])( cliente, self.grupo, message );
            comando_retorno = Comando(js["modulo"], js["comando"], js["funcao"], retorno_metodo );
            criptografia = "&1&";
            if js["comando"] != "ChaveSimetricaComando":
                criptografia = "&2&";
            self.grupo.add_envio(cliente, js["modulo"], js["comando"], js["funcao"], data=retorno_metodo, retorno="", criptografia=criptografia);
        except KeyboardInterrupt:
            return;
        except:
            traceback.print_exc();

    def disconnect(self):
        self.stop_enviador = True;
        self.stop_recebedor = True;
        self.connection.disconnect();

if __name__ == '__main__': 
    #logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s');
    configuracao = [];
    if os.path.exists(os.path.expanduser("~/.ggh_server_desenv.json")):
        configuracao =  open( os.path.expanduser("~/.ggh_server_desenv.json") ).readlines() ;
    else:
        configuracao.append( input("Informe o endereço XMPP do grupo: ") );
        configuracao.append( input("Informe o password: ") );
    xmpp_var = XMPPServer( configuracao[0].strip() , configuracao[1].strip() );
    if xmpp_var.conectar():
        print("Conectado");
        xmpp_var.pausa_enviador = False;
        xmpp_var.pausa_recebedor = False;
    #xmpp = ServidorGrupo( configuracao[0].strip() , configuracao[1].strip() );
    #xmpp.register_plugin('xep_0030') # Service Discovery
    #xmpp.register_plugin('xep_0004') # Data Forms
    #xmpp.register_plugin('xep_0060') # PubSub
    #xmpp.register_plugin('xep_0199') # XMPP Ping
    #xmpp.connect();
    #xmpp.process();











