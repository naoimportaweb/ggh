import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import   QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from classes.mural import Mural;
from form.form_mural_adicionar import FormMuralAdicionar;
from form.form_mural_ver import FormMuralVer;
from form.funcoes import Utilitario;

class PainelForumThread(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.threads = [];
        self.form_layout = QVBoxLayout( self );
        self.form_layout.addWidget(QLabel("Thread"));
        self.table = Utilitario.widget_tabela(self, ["Título", "-"], tamanhos=[], double_click=self.table_double_click);
        self.form_layout.addWidget( self.table );
        self.setLayout(self.form_layout);
    
    def carregar(self):
    	return;
    	#self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_topicos", {} );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ForumComando" and conteudo_js["funcao"] == "listar_thread":
            self.threads = [];
    
    def table_double_click(self):
    	return;