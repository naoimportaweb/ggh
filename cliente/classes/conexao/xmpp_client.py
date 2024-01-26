import xmpp, time, traceback, os, sys, inspect, traceback, threading, base64, importlib

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
        self.message_list_send = [];
        self.password = password;
        self.connection = None;
        self.callback = None;
        self.grupo = Grupo(jid_grupo);
        self.chave_criptografia = chave_criptografia;
        self.thread_enviador = None;
        self.thread_recebedor = None;
        self.stop_enviador = True;
        self.stop_recebedor = True;
        # TODA VEZ QUE SE GERA O OBJETO CRIA UM PAR DE CHAVE DIFERENTE;
        #           https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples
        self.cliente = Cliente( jid_participante, self.grupo  );
        self.cliente.criar_chaves();

    def conectar(self):
        jid = xmpp.protocol.JID( self.cliente.jid );
        self.connection = xmpp.Client(server=jid.getDomain(), debug=False);
        #self.connection.connect(proxy={'host':'127.0.0.1', 'port':'9051'});
        self.connection.connect();
        if self.connection.auth(user=jid.getNode(), password=self.password, resource=jid.getResource()) != None:
            self.connection.sendInitPresence();
            self.connection.RegisterHandler('message', self.processar_mensagem);

            self.stop_enviador = False;
            self.stop_recebedor = False;
            self.thread_recebedor = threading.Thread(target = self.escutar, args=());
            self.thread_recebedor.start();
            self.thread_enviador = threading.Thread(target = self.enviador, args=());
            self.thread_enviador.start();
            comando = Comando("comandos.chave_simetrica"  ,"ChaveSimetrica", "gerar", {"chave" : self.cliente.chave_publica() });
            mensagem = Mensagem( self.cliente, self.cliente.jid, self.grupo.jid);
            # -------1-------------------------------- GERAR NOVA CHAVE PÚBLICA E ENVIAR AQUI------------------------->
            msg_xmpp = xmpp.Message( to=self.grupo.jid, body=mensagem.criar( comando ) );
            msg_xmpp.setAttr('type', 'chat');
            self.connection.send( msg_xmpp );
            # <------2-------------------------------- RECEBER CHAVE SIMÉTRICA E GUARDAR, guardar em self.chave_servidor------------------------------
            return True;
        return False;
    
    def set_callback(self, callback):
        self.callback = callback;

    def adicionar_mensagem(self, modulo, comando, funcao, data, criptografia="&2&"):
        comando_objeto = Comando(modulo, comando, funcao, data);
        mensagem_objeto = Mensagem( self.cliente, self.cliente.jid, self.grupo.jid, comando=comando_objeto);
        self.message_list_send.append( mensagem_objeto );

    # quando loga, tem que atualizar algumas coisas
    def atualizar_entrada(self):
        self.adicionar_mensagem( "comandos.html" ,"Html", "get", {"path" : "regras.html"});
        self.adicionar_mensagem( "comandos.cliente_cadastro" ,"ClienteCadastro", "cadastro", {});
        self.adicionar_mensagem( "comandos.grupo_cadastro" ,"GrupoCadastro", "lista_clientes", {});
    
    def escutar(self):
        while True:
            try:
                if self.stop_recebedor:
                    return;
                self.connection.Process(1);
            except KeyboardInterrupt:
                return;
            except:
                print(".", end="");
            time.sleep(1);

    def enviador(self):
        while True:
            try:
                if self.stop_enviador:
                    return;
                if len(self.message_list_send) > 0 and self.cliente.chave_servidor != None:
                    mensagem = self.message_list_send.pop();
                    if mensagem != None:
                        msg_xmpp = xmpp.Message( to=self.grupo.jid, body=mensagem.toString() );
                        msg_xmpp.setAttr('type', 'chat');
                        self.connection.send( msg_xmpp );
            except KeyboardInterrupt:
                return;
            except:
                print(".", end="");
                traceback.print_exc(); 
            time.sleep(1);   
    
    def processar_mensagem(self, conn, mess):
        try:
            if self.callback == None:
                return;
            text = mess.getBody();
            if text == None:
                return;
            user=mess.getFrom();
            message = Mensagem( self.cliente, mess['to'], self.grupo.jid );
            message.fromString( text );
            js = message.toJson();
            MyClass = getattr(importlib.import_module(js["modulo"]), js["comando"]);
            instance = MyClass();
            #retorno = instance.processar( self.cliente, message ); 
            #retorno = getattr(instance, "retorno")( self.cliente, message );
            retorno = getattr(instance, js["funcao"])( self.cliente, self.grupo, message  );
            if retorno != None and self.callback != None:
                self.callback( user, retorno );
        except KeyboardInterrupt:
            return;
        except:
            traceback.print_exc();

    def disconnect(self):
        self.stop_enviador = True;
        self.stop_recebedor = True;
        self.connection.disconnect();

