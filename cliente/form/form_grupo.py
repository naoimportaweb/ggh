import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout;
from PySide6 import QtWidgets;
from PySide6.QtCore import Qt

from form.painel_chat import PainelChat
from form.painel_regras import PainelRegras
from form.painel_recomendacoes import PainelRecomendacoes
from form.painel_conhecimento import PainelConhecimento

class FormGrupo(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs);
        self.xmpp_var = None;

        self.layout1 = QVBoxLayout()

        self.b4 = QPushButton("Chat")
        self.b4.clicked.connect( self.botao_chat_click )
        self.layout1.addWidget(self.b4)

        self.b5 = QPushButton("Regras")
        self.b5.clicked.connect( self.botao_regras_click )
        self.layout1.addWidget(self.b5)

        self.b6 = QPushButton("Recomendações")
        self.b6.clicked.connect( self.botao_recomendacoes_click )
        self.layout1.addWidget(self.b6)

        self.b7 = QPushButton("Conhecimento")
        self.b7.clicked.connect( self.botao_conhecimento_click )
        self.layout1.addWidget(self.b7)

        self.layout1.addStretch();

        self.layout = QHBoxLayout();
        self.layout.addLayout( self.layout1 );
        self.setLayout( self.layout );
    
    def botao_conhecimento_click(self):
        self.layout.addWidget( self.conhecimento );
        self.regras.setParent( None );
        self.recomendacoes.setParent( None );
        self.chat.setParent( None );
        self.conhecimento.atualizar_tela();

    def botao_chat_click(self):
        self.layout.addWidget( self.chat );
        self.regras.setParent( None );
        self.recomendacoes.setParent( None );
        self.conhecimento.setParent( None );
    
    def botao_regras_click(self):
        self.layout.addWidget( self.regras );
        self.chat.setParent( None );
        self.recomendacoes.setParent( None );
        self.conhecimento.setParent( None );
    
    def botao_recomendacoes_click(self):
        self.layout.addWidget( self.recomendacoes );
        self.chat.setParent( None );
        self.regras.setParent( None );
        self.conhecimento.setParent( None );

    def set_grupo(self, xmpp_var):
        self.xmpp_var = xmpp_var;
        self.xmpp_var.set_callback(self.evento_mensagem);
        self.setWindowTitle( xmpp_var.cliente.jid +  " <=#=> " +  xmpp_var.grupo.jid );
        self.xmpp_var.atualizar_entrada();

    def carregar_panel( self ):
        self.chat =          PainelChat(self.xmpp_var);
        self.regras =        PainelRegras(self.xmpp_var);
        self.recomendacoes = PainelRecomendacoes(self.xmpp_var);
        self.conhecimento =  PainelConhecimento( self.xmpp_var );
        self.layout.addWidget( self.chat );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        self.chat.evento_mensagem(de, texto, message, conteudo_js);
        self.conhecimento.evento_mensagem(de, texto, message, conteudo_js);
    
    def closeEvent(self, event):
        event.accept();
        print("..:: FECHANDO:", self.xmpp_var.cliente.jid, "::..");
        self.xmpp_var.disconnect();
        self.xmpp_var = None;