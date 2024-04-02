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
        
        # TODA VEZ QUE SE GERA O OBJETO CRIA UM PAR DE CHAVE DIFERENTE;
        #           https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples
        self.cliente = Cliente( jid_participante, self.grupo, chave_local=chave_criptografia );
        self.cliente.password = password;

    def proxy(self, protocol, ip, port):
        ip_sem_tunel_proxy = requests.get('https://api.ipify.org').text;
        proxy = protocol + "://"+ ip +":" + str( port );
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        ip_com_tunel_proxy = requests.get('https://api.ipify.org').text;
        return ip_com_tunel_proxy != ip_sem_tunel_proxy;

    def conectar(self):
        jid = xmpp.protocol.JID( self.cliente.jid );
        self.connection = xmpp.Client(server=jid.getDomain(), debug=False);
        #self.connection.connect(proxy={'host':'127.0.0.1', 'port':'9051'});
        #self.connection.connect(proxy={'host':'127.0.0.1', 'port':'80'}, secure=0,use_srv=True);
        self.connection.connect();
        if self.connection.auth(user=jid.getNode(), password=self.password, resource=jid.getResource()) != None:
            self.connection.sendInitPresence();
            self.connection.RegisterHandler('message', self.processar_mensagem);
            time.sleep(5);
            self.stop_enviador = False;
            self.stop_recebedor = False;
            self.thread_recebedor = threading.Thread(target = self.escutar, args=());
            self.thread_recebedor.start();
            self.thread_enviador = threading.Thread(target = self.enviador, args=());
            self.thread_enviador.start();
            # abaixo tem um parametro chamado HOST que não serve para coisa alguma no código, serve só para pessoas curiosas se ferrarem tentando identificar o que é
            comando = Comando("comandos.grupo_cadastro"  ,"GrupoCadastroComando", "participar", {"chave" : self.cliente.chave_publica(), "host" : str( uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) ) )  });
            mensagem = Mensagem( self.cliente, self.cliente.jid, self.grupo.jid, comando=comando, criptografia="&0&");
            # -------1-------------------------------- GERAR NOVA CHAVE PÚBLICA E ENVIAR AQUI------------------------->
            mensagem.enviar( self.connection );
            # <------2-------------------------------- RECEBER CHAVE SIMÉTRICA E GUARDAR, guardar em self.chave_servidor------------------------------
            return True;
        return False;
    
    def set_callback(self, callback):
        self.callback = callback;
    
    def adicionar_mensagem(self, modulo, comando, funcao, data, criptografia="&2&", callback=None):
        self.pausa_enviador = True;
        self.grupo.adicionar_mensagem(self.cliente, modulo, comando, funcao, data, criptografia=criptografia, callback=callback);
        self.pausa_enviador = False;

    # quando loga, tem que atualizar algumas coisas
    #def atualizar_entrada(self):
    #    self.adicionar_mensagem( "comandos.html" ,"HtmlComando", "get", {"path" : "regras.html"});
    #    self.adicionar_mensagem( "comandos.html" ,"HtmlComando", "get", {"path" : "recomendacao.html"});
    #    self.adicionar_mensagem( "comandos.cliente_cadastro" ,"ClienteCadastroComando", "cadastro", {});
    #    self.adicionar_mensagem( "comandos.grupo_cadastro" ,"GrupoCadastroComando", "cadastro", {});
    
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
                traceback.print_exc();
            if len(self.grupo.message_list_send) == 0 or self.cliente.chave_servidor == None or self.pausa_enviador == True:
                time.sleep( 5 );   
    
    def processar_mensagem(self, conn, mess):
        try:
            if self.callback == None:
                return;
            text = mess.getBody();
            if text == None:
                return;
            user=mess.getFrom();
            message = Mensagem( self.cliente, mess['to'], self.grupo.jid );
            if message.fromString( text ):
                js = message.toJson( );
                #p rint("\033[91mChegou reposta:", js["modulo"],  js["comando"], js["funcao"], "\033[0m");
                MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"]);
                instance = MyClass();
                retorno = getattr(instance, js["funcao"])( self.cliente, self.grupo, message );
                if retorno != None and self.callback != None:
                    self.callback( user, retorno, message, js );
                
                index_aguardando_resposta = -1;
                for i in range(len(self.grupo.aguardando_resposta)):
                    if self.grupo.aguardando_resposta[i].id == message.id:
                        index_aguardando_resposta = i;
                        break;
                if index_aguardando_resposta >= 0:
                    buffer = self.grupo.aguardando_resposta.pop( index_aguardando_resposta );
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

