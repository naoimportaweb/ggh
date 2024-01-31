import time;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QListWidget, QListWidgetItem, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QHBoxLayout, QVBoxLayout, QMenuBar, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtCore import Qt

from api.fsseguro import FsSeguro

class PainelChat(QtWidgets.QWidget):
    def __init__( self, xmpp_var):
        super().__init__();
        self.xmpp_var = xmpp_var;
        form_layout = QHBoxLayout( self );
        self.lw = QListWidget()
        form_layout.addWidget( self.lw );

        form_layout_chat = QVBoxLayout( self );
        area = QPlainTextEdit(self);
        elemento = QPlainTextEdit(self);
        elemento.setMaximumHeight(100);
        form_layout_chat.addWidget(area);
        form_layout_chat.addWidget(elemento);
        form_layout.addLayout(form_layout_chat);
        self.setLayout( form_layout );
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
    
    def evento_mensagem(self, de, texto, message, conteudo_js):
        #html = self.fs.ler_raw( self.path_regra );
        print("Atualizar regras.");
        #if conteudo_js["comando"] == "Html":
        #    html = self.fs.ler_raw( self.path_regra );
        #    self.tb.setHtml(html);
            

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
        self.regras.evento_mensagem(de, texto, message, conteudo_js);
        self.chat.evento_mensagem(de, texto, message, conteudo_js);
    def __del__(self):
        self.xmpp_var.disconnect();
        self.xmpp_var = None;