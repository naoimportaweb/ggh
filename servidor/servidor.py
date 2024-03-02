#!/usr/bin/python3
import  logging, json, os, sys, inspect, base64, uuid, time, threading, importlib, requests;
import xmpp, time, traceback, os, sys, inspect, traceback, threading, base64, importlib, uuid;

#   https://github.com/xmpppy/xmpppy                                                                        TEORIA
#   https://stackoverflow.com/questions/16563200/connecting-to-jabber-server-via-proxy-in-python-xmppy      PROXY

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

class XMPPServer:
    def __init__(self, jid_server, password):
        self.inicializacao = str( uuid.uuid5(uuid.NAMESPACE_URL, jid_server + password + str(time.time())) )[0:16];
        self.grupo = Grupo( jid_server , self.inicializacao);
        #self.online = {};
        self.password = password;
        self.pausa_enviador = True; # inicamos pausados a thread, pois não estamos logados ainda.
        self.pausa_recebedor = True; # inicamos pausados a thread, pois não estamos logados ainda.
        self.connection = None;     # pipe de conexão com servidor XMPP remoto

    def conectar(self):
        jid = xmpp.protocol.JID( self.grupo.jid );
        self.connection = xmpp.Client(server=jid.getDomain(), debug=False); #debug="always"
        #self.connection.connect( server=("133.125.37.233", 5222 ), proxy={'host':'127.0.0.1', 'port': 9051}, secure=1  );
        self.connection.connect( );
        if self.connection.auth(user=jid.getNode(), password=self.password, resource=jid.getResource()) != None:
            print("Conectado.");
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
                        if not self.connection.isConnected(): self.connection.reconnectAndReauth()
                        print("Enviado:", mensagem.comando.comando);
                        print(" [+] from:", self.grupo.jid ," to:", mensagem.jid_to);
                        mensagem.enviar( self.connection );
                        #msg_xmpp = xmpp.Message( to=mensagem.jid_to , body=mensagem.toString() );
                        #msg_xmpp.setAttr('type', 'chat');
                        #self.connection.send( msg_xmpp );
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
            cliente = self.grupo.cliente( user );
            
            message = Mensagem( cliente,  user, self.grupo.jid ); # cliente, jid_from, jid_to
            if message.fromString( text ):
                js = message.toJson( );
                MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"])
                instance = MyClass()
                retorno_metodo = getattr(instance, js["funcao"])( cliente, self.grupo, message );
                comando_retorno = Comando(js["modulo"], js["comando"], js["funcao"], retorno_metodo );
                criptografia = "&2&";
                if js["comando"] == "GrupoCadastroComando" and js["funcao"] == "participar": # uma gambiarra, mas funciona. A primeira conexAo nao tem uma chave comum.
                    criptografia = "&1&";
                self.grupo.add_envio(cliente, js["modulo"], js["comando"], js["funcao"], data=retorno_metodo, retorno="", criptografia=criptografia);
        except KeyboardInterrupt:
            return;
        except:
            traceback.print_exc();

    def disconnect(self):
        self.stop_enviador = True;
        self.stop_recebedor = True;
        self.connection.disconnect();


# Obtendo arquivo de configuração < ========================================================
configuracao = None;
if os.path.exists(os.path.expanduser("~/.ggh_server_desenv.json")):
    configuracao =  json.loads( open( os.path.expanduser("~/.ggh_server_desenv.json") ).read() ) ;
else:
    configuracao = {
        "xmpp" :     { "server" :  "", "account" : "", "password" : ""},
        "database" : { "server" :  "", "user" :    "", "password" : "", "database" : "" },
        "proxy" :    {"protocol" : "", "server" :  "", "port" : 80 }
    };
    print("\033[94m" , "====== CONFIGURAÇÃO DO SERVIÇO JABBER ======" , "\033[0m");
    configuracao["xmpp"]["server"] =   input("Informe o endereço do servidor XMPP: ") ;
    configuracao["xmpp"]["account"] =  input("Informe o usuário do serviço XMPP: ") ;
    configuracao["xmpp"]["password"] = input("Informe o password: ") ;

    print("\033[94m" , "====== CONFIGURAÇÃO DO BANCO DE DADOS ======" , "\033[0m");
    configuracao["database"]["server"]   = input("Informe o IP do servidor mysql: ") ;
    configuracao["database"]["user"]     = input("Informe o usuário do serviço mysql: ") ;
    configuracao["database"]["password"] = input("Informe o password do serviço mysql: ") ;
    configuracao["database"]["database"] = input("Informe o Database do grupo: ") ;

    print("\033[94m" , "====== CONFIGURAÇÃO DO BANCO DE DADOS ======" , "\033[0m");
    configuracao["proxy"]["protocol"] = input("Informe o protocolo do proxy, pode ser http ou https: ") ;
    configuracao["proxy"]["server"]   = input("Informe o IP do proxy: ") ;
    configuracao["proxy"]["port"]     = int(input("Informe a porta: ")) ;

    if input("DESEJA salvar esta configuração (pressione s para SIM, e n para NÃO): ") == "s":
        with open(os.path.expanduser("~/.ggh_server_desenv.json"), "w") as f:
            f.write( json.dumps( configuracao ) );

# criando tabelas antes de iniciar o servidor
# Vamos jogar no environment os dados para conexão com MYSQL
os.environ["database"] = json.dumps( configuracao["database"] );
my = MysqlHelp();
print("- Testando o Banco de Dados.");
if my.teste() > 0:
    print("Você tem que corrigir os erros relacionados a falta de tabela/colunas no banco de dados.");
    sys.exit(1);
my = None;

# TESTANDO SEU IP, não pode ser o mesmo
ip_sem_tunel_proxy = requests.get('https://api.ipify.org').text;
proxy = configuracao["proxy"]["protocol"] + "://"+ configuracao["proxy"]["server"] +":" + str( configuracao["proxy"]["port"] );
os.environ['http_proxy'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy
ip_com_tunel_proxy = requests.get('https://api.ipify.org').text;
if ip_com_tunel_proxy == ip_sem_tunel_proxy:
    print("\033[95m", "Você não está usando proxy para realizar a conexão." , "\033[0m");
    sys.exit(1);
else:
    print("\033[95mIP após proxy:", ip_com_tunel_proxy , "\033[0m");

if __name__ == '__main__': 
    xmpp_var = XMPPServer( configuracao["xmpp"]["account"] , configuracao["xmpp"]["password"] );
    if xmpp_var.conectar():
        xmpp_var.pausa_enviador = False;
        xmpp_var.pausa_recebedor = False;












