
import xmpp, time, traceback
import threading, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
#import binascii

from api.aeshelp import AesHelper;

#   https://github.com/xmpppy/xmpppy                                                                        TEORIA
#   https://stackoverflow.com/questions/16563200/connecting-to-jabber-server-via-proxy-in-python-xmppy      PROXY

class XMPPCliente:

    def __init__(self, jid_participante, password, jid_grupo, chave_criptografia):
        self.message_list_send = [];
        self.jid_participante = jid_participante;
        self.password = password;
        self.connection = None;
        self.callback = None;
        self.jid_grupo = jid_grupo;
        self.chave_criptografia = chave_criptografia;
        self.chave_servidor = None;
        self.thread_enviador = None;
        self.thread_recebedor = None;
        self.stop_enviador = True;
        self.stop_recebedor = True;
        # TODA VEZ QUE SE GERA O OBJETO CRIA UM PAR DE CHAVE DIFERENTE;
        #           https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples
        self.key_pair = RSA.generate(3072);

    def conectar(self):
        jid = xmpp.protocol.JID( self.jid_participante );
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
            # -------1-------------------------------- GERAR NOVA CHAVE PÚBLICA E ENVIAR AQUI------------------------->
            public_key = self.key_pair.publickey();
            pubKeyPEM = public_key.exportKey();
            msg = xmpp.Message(to=self.jid_grupo, body=pubKeyPEM.decode());
            msg.setAttr('type', 'chat');
            self.connection.send(msg);
            #if os.path.exists(self.path_to_public):
            #    with open(self.path_to_public, "rb") as k:
            #        self.key_pub = RSA.importKey(k.read());
            # <------2-------------------------------- RECEBER CHAVE SIMÉTRICA E GUARDAR, guardar em self.chave_servidor------------------------------
            return True;
        return False;
    
    def set_callback(self, callback):
        self.callback = callback;
    
    def __criptografar__(self, mensagem):
        aes_help = AesHelper(key=self.chave_servidor );
        return aes_help.encrypt(mensagem).decode();
    
    def __descriptografar__(self, mensagem_criptografada):
        if self.chave_servidor == None:
            # usar a chave privada para descriptografar
            print("-----------------------------------------------------");
            print(mensagem_criptografada);
            print("-----------------------------------------------------");
            decryptor = PKCS1_OAEP.new(self.key_pair)
            decrypted = decryptor.decrypt( base64.b64decode( mensagem_criptografada.encode() ) ).decode();
            print("A chave simétrica será: ", decrypted);
            self.chave_servidor = decrypted;
            #self.chave_servidor = "2222222222222222";
            return None;
        else:
            # usar a chave simétrica para descripgrafar, ela é self.chave_servidor
            aes_help = AesHelper(key=self.chave_servidor );
            return aes_help.decrypt( mensagem_criptografada );

    def adicionar_mensagem(self, xmpp_acao):
        self.message_list_send.append( {"receiver" : self.jid_grupo, "message" : xmpp_acao.message } );

    def teste(self):
        self.message_list_send.append( {"receiver" : self.jid_grupo, "message" : '{"comando" : 1, "request" : "index.html" }' } );

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
                if len(self.message_list_send) > 0 and self.chave_servidor != None:
                    elemento = self.message_list_send.pop();
                    if elemento != None:
                        criptografado = self.__criptografar__(elemento["message"]);
                        msg = xmpp.Message(to=elemento["receiver"], body=criptografado );
                        print("será enviado: ", criptografado );
                        msg.setAttr('type', 'chat')
                        self.connection.send(msg)
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
            retorno_descriptografado = self.__descriptografar__(text);
            if retorno_descriptografado != None:
                self.callback( user, retorno_descriptografado );
        except KeyboardInterrupt:
            return;
        except:
            traceback.print_exc();

    def disconnect(self):
        self.stop_enviador = True;
        self.stop_recebedor = True;
        self.connection.disconnect();

#xmpp_var = XMPPCliente("hacker.cliente.1@xmpp.jp", "UmaSenhaIdiota1!");
#print(xmpp_var.conectar());
#def processar_callback(jid_participante, message):
#    print(jid_participante, message);
#def main():
#    xmpp = XMPPClient("hacker.cliente.1@xmpp.jp", "UmaSenhaIdiota1!");
#    xmpp.conectar(processar_callback);
#    for i in range(1000):
#        print(i);
#        xmpp.message_list_send.append({"receiver" : "nao.importa.web@jabb3r.de", "message" : "Teste 13 - " + str(i) });
#        time.sleep(10);
#if __name__ == "__main__":
#    main()
