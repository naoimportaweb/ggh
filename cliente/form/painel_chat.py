import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QScrollArea, QFrame, QMessageBox, QPlainTextEdit, QLabel, QListWidget, QListWidgetItem, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QHBoxLayout, QVBoxLayout, QMenuBar, QTextBrowser;
from PySide6.QtWidgets import QSizePolicy, QSizePolicy;
from PySide6 import QtWidgets;
from PySide6.QtCore import Qt, QObject
from PySide6.QtCore import  QFileSystemWatcher, QSettings, Signal, Slot, QThread;

from api.fsseguro import FsSeguro
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from api.chachahelp import ChaChaHelper;
from api.rsahelp import RsaHelper;


#https://gist.github.com/jazzycamel/8abd37bf2d60cce6e01d
class ThreadAtualizacaoChat(QObject):
    result= Signal(int)
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
    
    @Slot()
    def start(self): print("Iniciando atualização de chat a cada 5 segundos.")
    
    @Slot(int)
    def contador(self, n):
        while True:
            try:
                self.result.emit(n);
            except KeyboardInterrupt:
                sys.exit(0);
            except:
                traceback.print_exc();
            time.sleep(n);

class WidgetChatTexto(QtWidgets.QWidget):
    def __init__( self, texto, mensagem):
        super().__init__();
        frame = QFrame();
        frame.setFrameShape(QFrame.StyledPanel);

        if mensagem['id_remetente'] == mensagem['id_destinatario']:
            frame.setStyleSheet("background-color: lightyellow");
        else:
            frame.setStyleSheet("background-color: white");
        frame.setLineWidth(3)
        form_layout_chat = QVBoxLayout( frame );
        lbl_remetente = QLabel( self );
        if mensagem['id_remetente'] == mensagem['id_destinatario']:
            lbl_remetente.setText( "<b><font color='black'>Eu: </font><font color='red'>"+ mensagem["apelido_remetente"] +"</font></b>" );
        else:
            lbl_remetente.setText( "<b><font color='black'>Remetente: </font><font color='red'>"+ mensagem["apelido_remetente"] +"</font></b>" );
        lbl_mensagem = QLabel(self);
        lbl_mensagem.setStyleSheet("color: black");
        lbl_mensagem.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum);
        lbl_mensagem.setWordWrap(True);
        lbl_mensagem.setText(texto);
        lbl_mensagem.setGeometry(10,0,32,32)
        form_layout_chat.addWidget( lbl_remetente );
        form_layout_chat.addWidget( lbl_mensagem  );

        buffer = QVBoxLayout(self);
        buffer.addWidget(frame);
        self.setLayout( buffer );

class PainelChat(QtWidgets.QWidget):
    thread_atualizacao_chat= Signal(int)
    def __init__( self, xmpp_var):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.mensagens_adicionadas_chat = [];
        #self.mensagens_remover = [];
        self.fs = FsSeguro( self.xmpp_var.cliente.chave_local );
        self.form_layout = QHBoxLayout( self );
        self.list_nivel = QListWidget()
        self.list_nivel.itemSelectionChanged.connect(self.list_nivel_selected)
        self.form_layout.addWidget( self.list_nivel );
        self.form_layout_chat = QVBoxLayout( self );

        self.scroll = QScrollArea(self);
        self.scroll.setWidgetResizable(True);
        self.scroll.setWidgetResizable( False );
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.scroll.setWidgetResizable(True);

        self.d_scroll_area_widget = QtWidgets.QWidget();
        self.scroll.setWidget(self.d_scroll_area_widget);

        self.area_adicionar_mensagem = QVBoxLayout( self.d_scroll_area_widget );
        self.txt_mensagem = QPlainTextEdit(self);
        self.txt_mensagem.setMaximumHeight(100);
        self.btn_envio = QPushButton("Enviar");
        self.btn_envio.setGeometry(10,0,32,32);
        self.btn_envio.clicked.connect( self.btn_envio_click );
        self.form_layout_chat.addWidget( self.scroll );
        self.form_layout_chat.addWidget(    self.txt_mensagem              );
        self.form_layout_chat.addWidget(    self.btn_envio);
        self.form_layout.addLayout(         self.form_layout_chat);
        #THREAD de atualização de chat:
        self._thread = QThread()
        self._threaded = ThreadAtualizacaoChat( result = self.evento_atualizacao_chat_tela );
        self.thread_atualizacao_chat.connect(    self._threaded.contador );
        self._thread.started.connect( self._threaded.start );
        self._threaded.moveToThread(  self._thread );
        qApp.aboutToQuit.connect(     self._thread.quit);
        self._thread.start();
        self.thread_atualizacao_chat.emit(5);
        #THREAD de download de mensagens do XMPP
        self.thread_download_mensagens = threading.Thread(target = self.download_mensagens, args=());
        self.thread_download_mensagens.start();
        #INICIANDO LAYOUT
        self.setLayout( self.form_layout );

    @Slot(int)
    def evento_atualizacao_chat_tela(self, prime):
        index = self.list_nivel.currentRow();
        if index != -1:
            self.mensagens( self.area_adicionar_mensagem )

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
    
    def list_nivel_selected(self):
        self.mensagens_adicionadas_chat = [];
        self.clearLayout(self.area_adicionar_mensagem);

    def mensagens(self, layout):
        if self.list_nivel.currentRow() < 0:
            return;
        nivel = self.xmpp_var.grupo.niveis[ self.list_nivel.currentRow() ].id;
        rsa = RsaHelper(self.xmpp_var.cliente.public_key, self.xmpp_var.cliente.private_key);
        if not os.path.exists(self.xmpp_var.cliente.path_mensagens + "/" + nivel):
            os.makedirs(self.xmpp_var.cliente.path_mensagens + "/" + nivel);
        arquivos = os.listdir( self.xmpp_var.cliente.path_mensagens + "/" + nivel );
        arquivos.sort();
        adicionados = 0;
        for arquivo in arquivos:
            if arquivo not in self.mensagens_adicionadas_chat:
                adicionados += 1;
                js = self.fs.ler_json(self.xmpp_var.cliente.path_mensagens + "/" + nivel + "/" + arquivo);
                buffer = rsa.decrypt( js["chave_simetrica_criptografada"] );
                chacha = ChaChaHelper( buffer );
                mensagem = chacha.decrypt( base64.b64decode( js["mensagem_criptografada"] ).decode("utf-8") );
                item = WidgetChatTexto(mensagem, js );
                layout.addWidget( item );
                self.mensagens_adicionadas_chat.append( arquivo );
        if adicionados > 0:
            try:
                self.scroll.verticalScrollBar().rangeChanged.connect( self.scrollToBottom, Qt.UniqueConnection );
            except:
                traceback.print_exc();

    def scrollToBottom(self):
        scrollBar = self.scroll.verticalScrollBar()
        scrollBar.rangeChanged.disconnect(self.scrollToBottom)
        scrollBar.setValue(scrollBar.maximum())

    def download_mensagens(self):
        while True:
            try:
                if self.xmpp_var.finalizado == True:
                    return;
                index = self.list_nivel.currentRow();
                if index != -1 and self.ativo:
                    self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"MensagemComando", "listar", { } );
            except KeyboardInterrupt:
                sys.exit(0);
            except:
                traceback.print_exc();
            time.sleep(30);
    
    def btn_envio_click(self):
        # solicitar clientes aqui.
        if self.txt_mensagem.toPlainText().strip() == "":
            QMessageBox.critical(None, "Falha no uso do sistema", "Você tem que escrever uma mensagem para enviar.", QMessageBox.Ok)
            return;
        if self.list_nivel.currentRow() < 0:
            QMessageBox.critical(None, "Falha no uso do sistema", "Selecione o nível na lista.", QMessageBox.Ok)
            return;
        if self.txt_mensagem.toPlainText().strip() != "":
            self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"MensagemComando", "lista_clientes_niveis", {"nivel" : self.xmpp_var.grupo.niveis[self.list_nivel.currentRow()].id } );
            self.txt_mensagem.setDisabled(True);
            self.btn_envio.setDisabled(True);
    
    def atualizar_tela(self):
        for nivel in self.xmpp_var.grupo.niveis:
            item = QListWidgetItem( "Nível: " + nivel.nome)
            if self.xmpp_var.cliente.nivel_posicao >= nivel.posicao:
                if self.xmpp_var.cliente.nivel_posicao >= nivel.posicao:
                    self.list_nivel.addItem(item)
        #self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"MensagemComando", "listar", {} );
        if self.list_nivel.currentRow() < 0:
            self.list_nivel.setCurrentRow(0);

    def evento_mensagem(self, de, texto, message, conteudo_js):
        #if conteudo_js["comando"] == "GrupoCadastroComando":
        #    for nivel in self.xmpp_var.grupo.niveis:
        #        item = QListWidgetItem( "Nível: " + nivel.nome)
        #        if self.xmpp_var.cliente.nivel_posicao >= nivel.posicao:
        #            if self.xmpp_var.cliente.nivel_posicao >= nivel.posicao:
        #                self.list_nivel.addItem(item)
        #    #self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"MensagemComando", "listar", {} );
        #    if self.list_nivel.currentRow() < 0:
        #        self.list_nivel.setCurrentRow(0);
        if conteudo_js["comando"] == "MensagemComando" and conteudo_js["funcao"] == "lista_clientes_niveis":
            #{'clientes': [{'id': '91d0cf8f3883a0dcb338d15a47b326c9', 'apelido': 'ok7HdegG', 'public_key': '-----BEGIN PUBLIC KEY-----END PUBLIC KEY-----', 'nivel': '4'}], 'comando': 'Mensagem', 'funcao': 'lista_clientes_niveis', 'modulo': 'comandos.mensagem'}
            for cliente in conteudo_js["clientes"]:
                try:
                    rsa = RsaHelper(  cliente["public_key"] );
                    chave_simetrica = str( uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(conteudo_js) + str(time.time()) ) )[0:16];
                    chave_simetrica_criptografada = rsa.encrypt( chave_simetrica );
                    chacha = ChaChaHelper( chave_simetrica );
                    mensagem_criptografada = base64.b64encode( chacha.encrypt( self.txt_mensagem.toPlainText().strip() ) );
                    envelope = {"apelido_remetente" : self.xmpp_var.cliente.apelido, "apelido_destinatario" : cliente["apelido"],
                            "nivel" : cliente["id_nivel"], "mensagem_criptografada" : mensagem_criptografada.decode(),
                            "chave_simetrica_criptografada" : chave_simetrica_criptografada };
                    self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"MensagemComando", "enviar", envelope );
                except:
                    traceback.print_exc();
            self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"MensagemComando", "listar", {} );
            self.txt_mensagem.setPlainText("");
            self.txt_mensagem.setDisabled(False);
            self.btn_envio.setDisabled(False);
        if conteudo_js["comando"] == "MensagemComando" and conteudo_js["funcao"] == "listar":
            # {'retorno': [{'id': 'jitCQ6rIdo9XoTxqqFdN', 'id 
            for mensagem in conteudo_js["retorno"]:
                path_nivel = self.xmpp_var.cliente.path_mensagens + "/" + mensagem["id_nivel"];
                if not os.path.exists(path_nivel):
                    os.makedirs( path_nivel );
                fs = FsSeguro( self.xmpp_var.cliente.chave_local );
                if fs.escrever_raw( path_nivel + "/" + mensagem["ordem"], json.dumps( mensagem ) ):
                    self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"MensagemComando", "delete", {"id_mensagem" : mensagem["id"]} );
                #self.mensagens( );

