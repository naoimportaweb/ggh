import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import   QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView, QTextBrowser;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from form.funcoes import Utilitario;
from form.form_forum_novo_thread import FormForumNovoThread;

class PainelForumThread(QtWidgets.QWidget):
    def __init__( self, xmpp_var, callback_volta, callback_avanca ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.callback_volta = callback_volta;
        self.callback_avanca = callback_avanca;
        self.threads = [];
        self.id_forum_topico = None;
        self.form_layout = QVBoxLayout( self );
        self.lb_titulo = QLabel("Thread");
        btn_voltar = QPushButton("< Voltar");
        btn_voltar.clicked.connect(self.btn_voltar_click);
        Utilitario.widget_linha(self, self.form_layout, [btn_voltar, self.lb_titulo], stretch_inicio=False, stretch_fim=True);
        self.table = Utilitario.widget_tabela(self, ["Título", "-"], tamanhos=None, double_click=self.table_double_click);
        self.form_layout.addWidget( self.table );
        self.btn_novo = QPushButton("Nova thread");
        self.btn_novo.clicked.connect( self.btn_novo_click );
        Utilitario.widget_linha(self, self.form_layout, [self.btn_novo], stretch_inicio=True);
        self.setLayout(self.form_layout);
    
    def carregar_topico(self, id_forum_topico, topico):
        self.id_forum_topico = id_forum_topico;
        self.lb_titulo.setText( "<b>Tópico: </b>" + topico["titulo"] );
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_threads", {"id_forum_topico" : id_forum_topico } );
    
    def atualizar_tela(self):
        self.threads = [];
        self.table.setRowCount(0);
        return;

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ForumComando" and conteudo_js["funcao"] == "listar_threads":
            self.threads = conteudo_js["listar_threads"];
            self.table.setRowCount(len(self.threads));
            for i in range(len(self.threads)):
                self.table.setItem( i, 0, QTableWidgetItem(      self.threads[i]["titulo"] ) );
                self.table.setItem( i, 1, QTableWidgetItem( str( self.threads[i]["total" ] ) ) );
    
    def btn_voltar_click(self):
        self.callback_volta();
    
    def table_double_click(self):
        thread = self.threads[ self.table.currentRow() ];
        self.callback_avanca( thread ); # oi item já nao existe mais aqui.
    
    def callback_novo_thread(self, titulo, texto, form):
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "criar_thread", {"id_forum_topico" : self.id_forum_topico, "titulo" : titulo, "texto" : texto} );
        form.close();
        self.xmpp_var.adicionar_mensagem( "comandos.forum" ,"ForumComando", "listar_threads", {"id_forum_topico" : self.id_forum_topico } );
    
    def btn_novo_click(self):
        f = FormForumNovoThread(self.xmpp_var, self.callback_novo_thread);
        f.exec();