import xmpp, time, traceback, os, sys, inspect, traceback, threading, base64, importlib, uuid, requests;

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);

sys.path.append(ROOT);
sys.path.append(CURRENTDIR);

from api.aeshelp import AesHelper;
from classes.cliente import Cliente;
from api.mensagem import Mensagem;
from classes.grupo import Grupo
from api.comando import Comando;

#   https://github.com/xmpppy/xmpppy                                                                        TEORIA
#   https://stackoverflow.com/questions/16563200/connecting-to-jabber-server-via-proxy-in-python-xmppy      PROXY

class XMPPCliente:

    def __init__(self, jid_participante, password, jid_grupo, chave_criptografia):
        self.password = password;
        self.connection = None;
        self.callback = None;
        self.grupo = Grupo(jid_grupo);
        self.chave_criptografia = chave_criptografia;
        self.thread_enviador = None;
        self.thread_recebedor = None;
        self.stop_enviador = True;
        self.stop_recebedor = True;
        self.finalizado = False;
        self.pausa_enviador = False;
        self.dados_basicos_carregados = False;
        
        # TODA VEZ QUE SE GERA O OBJETO CRIA UM PAR DE CHAVE DIFERENTE;
        #           https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples
        self.cliente = Cliente( jid_participante, self.grupo, chave_local=chave_criptografia );
        self.cliente.password = password;

    def proxy(self, protocol, ip, port):
        if ip == "" or protocol == "" or port == "":
            del os.environ['http_proxy']  ;
            del os.environ['https_proxy'] ;
            del os.environ['HTTP_PROXY']  ;
            del os.environ['HTTPS_PROXY'] ;
            return True;
        proxy = protocol + "://"+ ip +":" + str( port );
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        return True;

    def conectar(self):
        jid = xmpp.protocol.JID( self.cliente.jid );
        self.connection = xmpp.Client(server=jid.getDomain(), debug=False);
        #self.connection.connect(proxy={'host':'127.0.0.1', 'port':'9051'});
        #self.connection.connect(proxy={'host':'127.0.0.1', 'port':'80'}, secure=0,use_srv=True);
        self.connection.connect();
        if self.connection.auth(user=jid.getNode(), password=self.password, resource=jid.getResource()) != None:
            self.connection.sendInitPresence(requestRoster=0);
            self.connection.RegisterHandler('message', self.processar_mensagem);
            time.sleep(5);
            self.connection.sendPresence(jid=self.grupo.jid, typ="subscribed"); #https://stackoverflow.com/questions/8956804/xmpp-bot-accept-new-friend
            self.connection.sendPresence(jid=self.grupo.jid, typ="subscribe");  #https://stackoverflow.com/questions/8956804/xmpp-bot-accept-new-friend
            self.stop_enviador = False;
            self.stop_recebedor = False;
            self.thread_recebedor = threading.Thread(target = self.escutar, args=());
            self.thread_recebedor.start();
            self.thread_enviador = threading.Thread(target = self.enviador, args=());
            self.thread_enviador.start();
            # iniciar a chave.
            comando = Comando("comandos.grupo_cadastro"  ,"GrupoCadastroComando", "participar", {"chave" : self.cliente.chave_publica(), "host" : str( uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) ) )  });
            mensagem = Mensagem( self.cliente, self.cliente.jid, self.grupo.jid, comando=comando, criptografia="&0&");
            mensagem.enviar( self.connection );
            return True;
        return False;
    
    def callback_interno(self, de, texto, message, conteudo_js):
        
        if conteudo_js["comando"] == "ClienteCadastroComando" and conteudo_js["funcao"] == "cadastro":
            self.dados_basicos_carregados = True;
    
    def set_callback(self, callback):
        self.callback = callback;
    
    def adicionar_mensagem(self, modulo, comando, funcao, data, criptografia="&2&", callback=None):
        self.pausa_enviador = True;
        buffer_id = self.grupo.adicionar_mensagem(self.cliente, modulo, comando, funcao, data, criptografia=criptografia, callback=callback).id;
        self.pausa_enviador = False;
        return buffer_id;

    # quando loga, tem que atualizar algumas coisas
    def iniciar(self):   
        self.adicionar_mensagem( "comandos.cliente_cadastro" ,"ClienteCadastroComando", "cadastro", {});
        self.adicionar_mensagem( "comandos.grupo_cadastro" ,"GrupoCadastroComando", "cadastro", {});
    
    def escutar(self):
        while True:
            try:
                if self.stop_recebedor:
                    return;
                if self.connection.Process(1) == 0:
                    time.sleep(3);
            except KeyboardInterrupt:
                return;
            except:
                print(".", end="");
                time.sleep(5);
    
    def enviador(self):
        while True:
            try:
                if self.stop_enviador:
                    return;
                if len(self.grupo.message_list_send) > 0 and self.cliente.chave_servidor != None and self.pausa_enviador == False:
                    mensagem = self.grupo.message_list_send.pop(0);
                    if mensagem != None:
                        if not self.connection.isConnected(): self.connection.reconnectAndReauth()
                        mensagem.enviar( self.connection );
                        self.grupo.aguardando_resposta.append( mensagem );
                        time.sleep(0.1);
                elif len(self.grupo.message_list_send) > 0 and ( self.cliente.chave_servidor == None or self.pausa_enviador == True ):
                    print("\033[93mTem mensagem na fila, mas deu problema: \033[0m", "Existe chave:", self.cliente.chave_servidor != None, " Pausa: ", self.pausa_enviador);

            except KeyboardInterrupt:
                sys.exit(1);
            except:
                print(".", end="");
                time.sleep(3);
            if len(self.grupo.message_list_send) == 0 or self.cliente.chave_servidor == None or self.pausa_enviador == True:
                time.sleep( 5 );   
    
    def processar_mensagem(self, conn, mess):
        try:
            #if self.callback == None:
            #    print("callback null");
            #    return;
            text = mess.getBody();
            if text == None:
                print("Text null");
                return;
            user=mess.getFrom();
            message = Mensagem( self.cliente, mess['to'], self.grupo.jid );
            if message.fromString( text ):
                js = message.toJson( );
                print("\033[91mChegou reposta:", js["modulo"],  js["comando"], js["funcao"], "\033[0m");
                MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"]);
                instance = MyClass();
                retorno = getattr(instance, js["funcao"])( self.cliente, self.grupo, message );
                
                if retorno != None:
                    self.callback_interno(user, retorno, message, js);
                    if self.callback != None:
                        self.callback( user, retorno, message, js );
                
                index_aguardando_resposta = -1;
                for i in range(len(self.grupo.aguardando_resposta)):
                    if self.grupo.aguardando_resposta[i].id == message.id:
                        index_aguardando_resposta = i;
                        break;
                if index_aguardando_resposta >= 0:
                    buffer = self.grupo.aguardando_resposta.pop( index_aguardando_resposta ); #### aqqui tem que fazer o lance da thread ####
                    self.grupo.processados.append(message); # guardar no histórico.
                    if buffer.callback != None:
                        if type("") != type(buffer.callback):
                            buffer.callback(message);
        except KeyboardInterrupt:
            return;
        except:
            traceback.print_exc();

    def disconnect(self):
        self.stop_enviador = True;
        self.stop_recebedor = True;
        self.finalizado = True;
        #self.connection.disconnect();
        #sys.exit(0);

