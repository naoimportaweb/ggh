import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import   QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from form.painel_forum_thread import PainelForumThread;
from form.painel_forum_topico import PainelForumTopico;
from form.painel_forum_resposta import PainelForumResposta;

from form.funcoes import Utilitario;

class PainelForum(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        self.form_layout = QVBoxLayout( self );
        self.painel_topico = PainelForumTopico(    self.xmpp_var, self.carregar_topico );
        self.painel_thread = PainelForumThread(    self.xmpp_var, self.carregar       ,  self.carregar_thread    );
        self.painel_reposta = PainelForumResposta( self.xmpp_var, self.voltar_topico   );
        self.form_layout.addWidget( self.painel_topico );
        self.painel = 0;
        self.setLayout(self.form_layout);
    def carregar(self):
        self.painel = 0;
        self.form_layout.addWidget( self.painel_topico );
        self.painel_topico.atualizar_tela();
        self.painel_thread.setParent( None );
        self.painel_reposta.setParent( None );
        return;
    def carregar_topico(self, topico):
        self.painel = 1;
        self.form_layout.addWidget( self.painel_thread );
        self.painel_thread.atualizar_tela();
        self.painel_thread.carregar_topico(topico["id"], topico);
        self.painel_topico.setParent( None );
        self.painel_reposta.setParent( None )
    def carregar_thread(self, thread, id_forum_thread):
        self.painel = 2;
        self.form_layout.addWidget( self.painel_reposta );
        self.painel_reposta.atualizar_tela(  );
        self.painel_reposta.carregar_thread(thread, id_forum_thread);
        self.painel_topico.setParent( None );
        self.painel_thread.setParent( None );
    def voltar_topico(self):
        self.painel = 1;
        self.form_layout.addWidget( self.painel_thread );
        self.painel_topico.setParent( None );
        self.painel_reposta.setParent( None );
        return;
    def parar_tela(self):
        return;
    def atualizar_tela(self):
        if self.painel == 0:
            self.painel_topico.atualizar_tela();
        elif self.painel == 1:
            self.painel_thread.atualizar_tela();
        elif self.painel == 2:
            self.painel_reposta.atualizar_tela();
    def evento_mensagem(self, de, texto, message, conteudo_js):
        if self.painel == 0:
            self.painel_topico.evento_mensagem(de, texto, message, conteudo_js);
        elif self.painel == 1:
            self.painel_thread.evento_mensagem(de, texto, message, conteudo_js);
        elif self.painel == 2:
            self.painel_reposta.evento_mensagem(de, texto, message, conteudo_js);
    
