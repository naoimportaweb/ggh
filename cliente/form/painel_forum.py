import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import   QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from classes.mural import Mural;
from form.form_mural_adicionar import FormMuralAdicionar;
from form.form_mural_ver import FormMuralVer;
from form.painel_forum_topico import PainelForumTopico
from form.painel_forum_thread import PainelForumThread
from form.funcoes import Utilitario;

class PainelForum(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        self.topicos = [];
        self.form_layout = QVBoxLayout( self );
        self.painel_forum_topico = PainelForumTopico(xmpp_var);
        self.painel_forum_thread = PainelForumThread(xmpp_var);
        self.form_layout.addWidget( self.painel_forum_topico );
        self.form_layout.addWidget( self.painel_forum_thread );
        self.painel_forum_thread.setParent( None );
        self.setLayout(self.form_layout);
    
    def parar_tela(self):
        return;
    
    def atualizar_tela(self):
        self.painel_forum_topico.atualizar_tela();

    def evento_mensagem(self, de, texto, message, conteudo_js):
        self.painel_forum_topico.evento_mensagem(de, texto, message, conteudo_js);
    
    #def btn_novo_click(self):     
    #    f = FormMuralAdicionar( self.xmpp_var );
    #    f.exec();
    #    self.xmpp_var.adicionar_mensagem( "comandos.mural" ,"MuralComando", "listar", {} );
    #def table_mural_double(self):
    #    row = self.table.currentRow();
    #    f = FormMuralVer(self.xmpp_var, self.mensagens[row]);
    #    f.exec();