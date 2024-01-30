import time;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QHBoxLayout, QVBoxLayout, QMenuBar, QTextBrowser;
from PySide6 import QtWidgets;

from api.fsseguro import FsSeguro

class PainelChat(QtWidgets.QWidget):
    def __init__( self, xmpp_var):
        super().__init__();
        self.xmpp_var = xmpp_var;
        form_layout = QVBoxLayout( self );
        exemplo = QLineEdit('chat', self);
        form_layout.addWidget( exemplo );
        form_layout.addStretch();
        self.setLayout(form_layout);
        #self.setFixedWidth(600)
    
class PainelRegras(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        fs = FsSeguro( self.xmpp_var.cliente.chave_local );
        form_layout = QVBoxLayout( self );
        #exemplo = QLineEdit('regras', self);
        #form_layout.addWidget( exemplo );
        #form_layout.addStretch();
        #self.setLayout(form_layout);
        self.tb = QTextBrowser(self);
        self.tb.setAcceptRichText(True);
        self.tb.setOpenExternalLinks(False);
        self.tb.setHtml(fs.ler_raw( self.xmpp_var.grupo.path_grupo_html + "/regras.html" ));

        self.b4 = QPushButton("Atualizar")
        self.b4.setGeometry(10,0,32,32)
        self.b4.clicked.connect( self.botao_atualizar_click )
        

        form_layout.addWidget( self.tb );
        form_layout.addWidget( self.b4 );
        form_layout.addStretch();
        self.setLayout(form_layout);
        #self.setFixedWidth(600)
    def botao_atualizar_click(self):
        fs = FsSeguro( self.xmpp_var.cliente.chave_local );
        html = fs.ler_raw( self.xmpp_var.grupo.path_grupo_html + "/regras.html" );
        self.tb.setHtml(html);

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
        if message.callback_retorno != "":
            print("chamar: ", message.callback_retorno);
        #print(conteudo_js);
        #if conteudo_js["comando"] == "Html":
        #    print("aTUALIZAR HTML ");
        #    #self.regras.botao_atualizar_click();
    
    def __del__(self):
        self.xmpp_var.disconnect();
        self.xmpp_var = None;