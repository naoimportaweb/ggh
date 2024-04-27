import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import   QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from classes.mural import Mural;
from form.form_mural_adicionar import FormMuralAdicionar;
from form.form_mural_ver import FormMuralVer;
from form.form_forum_novo_topico import FormForumNovoTopico
from form.funcoes import Utilitario;


class PainelForumTopico(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.form_layout = QVBoxLayout( self );
        self.form_layout.addWidget(QLabel("Topico"));
        self.topicos = [];
        self.table = Utilitario.widget_tabela(self, ["Título", "-"], double_click=self.table_double_click);
        self.form_layout.addWidget( self.table );
        self.btn_novo = QPushButton("Novo tópico");
        self.btn_novo.clicked.connect( self.btn_novo_click );
        Utilitario.widget_linha(self, self.form_layout, [self.btn_novo], stretch_inicio=True);
        self.setLayout(self.form_layout);
    
    def atualizar_tela(self):
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_topicos", {} );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ForumComando" and conteudo_js["funcao"] == "listar_topicos":
            self.topicos = [];
            for i in range(len(self.topicos)):
                self.table.setItem( i, 0, QTableWidgetItem( self.topicos[i]["titulo"] ) );
                self.table.setItem( i, 1, QTableWidgetItem( self.topicos[i]["total"] ) );
        elif conteudo_js["comando"] == "ForumComando" and conteudo_js["funcao"] == "criar_topico":
        	self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_topicos", {} );
    def table_double_click(self):
        return;

    def callback_novo_topico(self, id_nivel, titulo, descricao, form):
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "criar_topico", {"id_nivel" : id_nivel, "titulo" : titulo, "descricao" : descricao} );
        form.close();

    def btn_novo_click(self):
        f = FormForumNovoTopico(self.xmpp_var, self.callback_novo_topico);
        f.exec();
