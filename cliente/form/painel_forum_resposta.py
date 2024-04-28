import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import  QFrame, QScrollArea, QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtWidgets import QSizePolicy, QSizePolicy;
from PySide6.QtCore import Qt, QObject, QTimer;
#from PySide6.QtCore import  QFileSystemWatcher, QSettings, Signal, Slot, QThread;

from form.funcoes import Utilitario;
from form.form_forum_nova_resposta import FormForumNovaResposta;

class PainelForumResposta(QtWidgets.QWidget):
    def __init__( self, xmpp_var, callback ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.callback = callback;
        self.thread = None;
        self.respostas = [];
        self.adicionados = [];
        self.id_forum_thread = None;
        self.form_layout = QVBoxLayout( self );
        self.lb_titulo = QLabel("Respostas");
        btn_voltar = QPushButton("< Voltar");
        btn_voltar.clicked.connect(self.btn_voltar_click);
        Utilitario.widget_linha(self, self.form_layout, [btn_voltar, self.lb_titulo], stretch_inicio=False, stretch_fim=True);


        self.text = QLabel(self);
        
        #self.form_layout.addWidget( self.text );

        self.scroll = QScrollArea(self);
        self.scroll.setWidgetResizable(True);
        self.scroll.setWidgetResizable( False );
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.scroll.setWidgetResizable(True);
        self.d_scroll_area_widget = QtWidgets.QWidget();
        self.scroll.setWidget(self.d_scroll_area_widget);
        self.area_adicionar_mensagem = QVBoxLayout( self.d_scroll_area_widget );
        self.form_layout.addWidget( self.scroll );
        

        self.btn_novo = QPushButton("Nova Resposta");
        self.btn_novo.clicked.connect( self.btn_novo_click );
        Utilitario.widget_linha(self, self.form_layout, [self.btn_novo], stretch_inicio=True);
        self.setLayout(self.form_layout);

        self.atualizar_lista = False; # problema de QT Thread e Python Thread....
        self.timer=QTimer();
        self.timer.timeout.connect(self.evento_atualizacao_tela);
        self.timer.start(1000);
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
    
    def evento_atualizacao_tela(self):
        if not self.atualizar_lista:
            return;
        self.atualizar_lista = False;
        
        for i in range(len( self.respostas )):
            if self.respostas[i]["id"] in self.adicionados:
                continue;
            self.adicionados.append( self.respostas[i]["id"] );
            r = WidgetResposta(self.xmpp_var, self.respostas[i]);
            self.area_adicionar_mensagem.addWidget( r );
        return;
    
    def carregar_thread(self, thread):
        self.clearLayout(self.area_adicionar_mensagem);
        self.id_forum_thread = thread["id"];
        self.text.setText(       thread["texto"]  );
        self.area_adicionar_mensagem.addWidget( self.text );
        self.lb_titulo.setText( "<b>Thread: </b> " + thread["titulo"] );
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_respostas", {"id_forum_thread" : thread["id"] } );
    
    def atualizar_tela(self):
        self.respostas = [];
        return;

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ForumComando" and conteudo_js["funcao"] == "listar_respostas":
            self.respostas = conteudo_js["forum_resposta"];
            self.atualizar_lista = True;
            
    
    def btn_voltar_click(self):
        self.callback();
    
    def callback_nova_resposta(self, texto, form):
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "criar_resposta", {"id_forum_thread" : self.id_forum_thread, "texto" : texto} );
        form.close();
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_respostas", {"id_forum_thread" : self.id_forum_thread } );
    
    def btn_novo_click(self):
        f = FormForumNovaResposta(self.xmpp_var, self.callback_nova_resposta);
        f.exec();

class WidgetResposta(QtWidgets.QWidget):
    def __init__( self, xmpp_var, resposta):
        super().__init__();
        frame = QFrame();
        #{"nome" : "forum_resposta", "fields" : ["id", "id_forum_thread", "id_cliente", "texto", "data_cadastro"]},
        frame.setFrameShape(QFrame.StyledPanel);

        if resposta['id_cliente'] == xmpp_var.cliente.id:
            frame.setStyleSheet("background-color: lightyellow");
        else:
            frame.setStyleSheet("background-color: white");
        frame.setLineWidth(3)
        form_layout_chat = QVBoxLayout( frame );
        lbl_remetente = QLabel( self );
        lbl_remetente.setText("");
        #if mensagem['id_remetente'] == mensagem['id_destinatario']:
        #    lbl_remetente.setText( "<b><font color='black'>Eu: </font><font color='red'>"+ mensagem["apelido_remetente"] +"</font></b>" );
        #else:
        #    lbl_remetente.setText( "<b><font color='black'>Remetente: </font><font color='red'>"+ mensagem["apelido_remetente"] +"</font></b>" );
        lbl_mensagem = QLabel(self);
        lbl_mensagem.setStyleSheet("color: black");
        lbl_mensagem.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum);
        lbl_mensagem.setWordWrap(True);
        lbl_mensagem.setText(resposta["texto"]);
        lbl_mensagem.setGeometry(10,0,32,32)
        form_layout_chat.addWidget( lbl_remetente );
        form_layout_chat.addWidget( lbl_mensagem  );

        buffer = QVBoxLayout(self);
        buffer.addWidget(frame);
        self.setLayout( buffer );