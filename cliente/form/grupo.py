import time, base64, uuid, os, sys, json;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QFrame, QPlainTextEdit, QLabel, QListWidget, QListWidgetItem, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QHBoxLayout, QVBoxLayout, QMenuBar, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtCore import Qt

from api.fsseguro import FsSeguro
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from api.chachahelp import ChaChaHelper;
from api.rsahelp import RsaHelper;


class WidgetChatTexto(QtWidgets.QWidget):
    def __init__( self, texto):
        super().__init__();
        frame = QFrame(self);
        frame.setStyleSheet("background-color: rgb(0, 0, 0)")
        frame.setLineWidth(3);
        form_layout_chat = QVBoxLayout( frame );
        label = QLabel(self);
        label.setText(texto);
        form_layout_chat.addWidget(label);
        self.setLayout( form_layout_chat );


class PainelChat(QtWidgets.QWidget):
    def __init__( self, xmpp_var):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.fs = FsSeguro( self.xmpp_var.cliente.chave_local );
        form_layout = QHBoxLayout( self );
        self.lw = QListWidget()
        form_layout.addWidget( self.lw );
        form_layout_chat = QVBoxLayout( self );
        self.area_adicionar_mensagem = QVBoxLayout( self );
        #area = QPlainTextEdit(self);
        self.txt_mensagem = QPlainTextEdit(self);
        self.txt_mensagem.setMaximumHeight(100);
        btn_envio = QPushButton("Enviar")
        btn_envio.setGeometry(10,0,32,32)
        btn_envio.clicked.connect( self.btn_envio_click )
        btn_atualizar = QPushButton("Atualizar")
        btn_atualizar.setGeometry(10,0,32,32)
        btn_atualizar.clicked.connect( self.btn_atualizar_click )
        form_layout_chat.addLayout(self.area_adicionar_mensagem);
        #form_layout_chat.addWidget(area);
        form_layout_chat.addWidget(self.txt_mensagem);
        form_layout_chat.addWidget(btn_envio);
        form_layout_chat.addWidget(btn_atualizar);
        form_layout.addLayout(form_layout_chat);
        #texto1 = WidgetChatTexto("Um texto simples.");
        #self.area_adicionar_mensagem.addWidget( texto1 );
        self.setLayout( form_layout );
    def btn_atualizar_click(self):
        self.mensagens("41f38c9c2383f414db6ce99f50cff9ad8");
        #self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"Mensagem", "listar", {"id_nivel" : nivel["id"]} );
    def mensagens(self, nivel):
        rsa = RsaHelper(self.xmpp_var.cliente.public_key, self.xmpp_var.cliente.private_key);
        if not os.path.exists(self.xmpp_var.cliente.path_mensagens + "/" + nivel):
            os.makedirs(self.xmpp_var.cliente.path_mensagens + "/" + nivel);
        arquivos = os.listdir( self.xmpp_var.cliente.path_mensagens + "/" + nivel );
        for arquivo in arquivos:
            js = self.fs.ler_json(self.xmpp_var.cliente.path_mensagens + "/" + nivel + "/" + arquivo);
            buffer = rsa.decrypt( js["chave_simetrica_criptografada"] );
            chacha = ChaChaHelper( buffer );
            mensagem = chacha.decrypt( base64.b64decode( js["mensagem_criptografada"] ).decode("utf-8") );
            print(mensagem);

    def btn_envio_click(self):
        # solicitar clientes aqui.
        if self.txt_mensagem.toPlainText().strip() != "":
            self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"Mensagem", "lista_clientes_niveis", {"nivel" : "41f38c9c2383f414db6ce99f50cff9ad8"} );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "GrupoCadastro":
            for nivel in self.xmpp_var.grupo.niveis:
                item = QListWidgetItem(nivel["nome"] + "("+ str(nivel["posicao"]) +")")
                if self.xmpp_var.cliente.nivel_posicao >= nivel["posicao"]:
                    if self.xmpp_var.cliente.nivel_posicao == nivel["posicao"]:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                self.lw.addItem(item)
                self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"Mensagem", "listar", {"id_nivel" : nivel["id"]} );
        if conteudo_js["comando"] == "Mensagem" and conteudo_js["funcao"] == "lista_clientes_niveis":
            #{'clientes': [{'id': '91d0cf8f3883a0dcb338d15a47b326c9', 'apelido': 'ok7HdegG', 'public_key': '-----BEGIN PUBLIC KEY-----END PUBLIC KEY-----', 'nivel': '4'}], 'comando': 'Mensagem', 'funcao': 'lista_clientes_niveis', 'modulo': 'comandos.mensagem'}
            for cliente in conteudo_js["clientes"]:
                rsa = RsaHelper(  cliente["public_key"] );
                chave_simetrica = str( uuid.uuid5(uuid.NAMESPACE_URL, "0fk") )[0:16];
                chave_simetrica_criptografada = rsa.encrypt( chave_simetrica );
                chacha = ChaChaHelper( chave_simetrica );
                mensagem_criptografada = base64.b64encode( chacha.encrypt( self.txt_mensagem.toPlainText() ) );
                envelope = {"apelido_remetente" : self.xmpp_var.cliente.apelido, "apelido_destinatario" : cliente["apelido"],
                        "nivel" : cliente["nivel"], "mensagem_criptografada" : mensagem_criptografada.decode(),
                        "chave_simetrica_criptografada" : chave_simetrica_criptografada };
                self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"Mensagem", "enviar", envelope );
            self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"Mensagem", "listar", {"id_nivel" : "41f38c9c2383f414db6ce99f50cff9ad8"} );
            self.txt_mensagem.setPlainText("");
        if conteudo_js["comando"] == "Mensagem" and conteudo_js["funcao"] == "listar":
            # {'retorno': [{'id': 'jitCQ6rIdo9XoTxqqFdN', 'id 
            for mensagem in conteudo_js["retorno"]:
                path_nivel = self.xmpp_var.cliente.path_mensagens + "/" + mensagem["id_nivel"];
                if not os.path.exists(path_nivel):
                    os.makedirs( path_nivel );
                fs = FsSeguro( self.xmpp_var.cliente.chave_local );
                if fs.escrever_raw( path_nivel + "/" + mensagem["ordem"], json.dumps( mensagem ) ):
                    self.xmpp_var.adicionar_mensagem( "comandos.mensagem" ,"Mensagem", "delete", {"id_mensagem" : mensagem["id"]} );
            #self.mensagens("41f38c9c2383f414db6ce99f50cff9ad8");

    
class PainelRegras(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.fs = FsSeguro( self.xmpp_var.cliente.chave_local );
        self.path_regra = self.xmpp_var.grupo.path_grupo_html + "/regras.html";
        form_layout = QVBoxLayout( self );
        self.tb = QTextBrowser(self);
        self.tb.setAcceptRichText(True);
        self.tb.setOpenExternalLinks(False);
        self.tb.setHtml(self.fs.ler_raw( self.path_regra ));
        self.b4 = QPushButton("Atualizar")
        self.b4.setGeometry(10,0,32,32)
        self.b4.clicked.connect( self.botao_atualizar_click )
        form_layout.addWidget( self.tb );
        form_layout.addWidget( self.b4 );
        form_layout.addStretch();
        self.setLayout(form_layout);
    
    def botao_atualizar_click(self):
        html = self.fs.ler_raw( self.path_regra );
        self.tb.setHtml(html);
    
    # futura implementácao
    #def evento_mensagem(self, de, texto, message, conteudo_js):
            

class FormGrupo(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs);
        self.xmpp_var = None;

        self.layout1 = QVBoxLayout()

        self.b4 = QPushButton("Chat")
        #self.b4.setGeometry(10,0,32,32)
        self.b4.clicked.connect( self.botao_chat_click )
        self.layout1.addWidget(self.b4)

        self.b5 = QPushButton("Regras")
        #self.b5.setGeometry(10,40,32,32)
        self.b5.clicked.connect( self.botao_regras_click )
        self.layout1.addWidget(self.b5)

        self.layout1.addStretch();

        self.layout = QHBoxLayout();
        self.layout.addLayout( self.layout1 );
        self.setLayout( self.layout );
    
    def botao_chat_click(self):
        self.layout.addWidget( self.chat );
        self.regras.setParent( None );
    def botao_regras_click(self):
        self.layout.addWidget( self.regras );
        self.chat.setParent( None );

    def set_grupo(self, xmpp_var):
        self.xmpp_var = xmpp_var;
        self.xmpp_var.set_callback(self.evento_mensagem);
        self.setWindowTitle( xmpp_var.grupo.jid );
        self.xmpp_var.atualizar_entrada();

    def carregar_panel( self ):
        self.chat = PainelChat(self.xmpp_var);
        self.regras = PainelRegras(self.xmpp_var);
        self.layout.addWidget( self.chat );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        #self.regras.evento_mensagem(de, texto, message, conteudo_js);
        self.chat.evento_mensagem(de, texto, message, conteudo_js);
    def __del__(self):
        self.xmpp_var.disconnect();
        self.xmpp_var = None;