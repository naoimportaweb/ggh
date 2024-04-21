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

class PainelForum(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        self.topicos = [];
        form_layout = QVBoxLayout( self );
        self.setLayout(form_layout);
    def parar_tela(self):
        return;
    def atualizar_tela(self):
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_topicos", {} );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ForumComando" and conteudo_js["funcao"] == "listar_topicos":
            self.topicos = [];
    
    #def btn_novo_click(self):     
    #    f = FormMuralAdicionar( self.xmpp_var );
    #    f.exec();
    #    self.xmpp_var.adicionar_mensagem( "comandos.mural" ,"MuralComando", "listar", {} );
    #def table_mural_double(self):
    #    row = self.table.currentRow();
    #    f = FormMuralVer(self.xmpp_var, self.mensagens[row]);
    #    f.exec();