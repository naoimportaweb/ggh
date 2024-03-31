import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *

from classes.mural import Mural;
from form.form_mural_adicionar import FormMuralAdicionar;
from form.form_mural_ver import FormMuralVer;

class PainelMural(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        form_layout = QVBoxLayout( self );
        self.mensagens = [];
        self.table = QTableWidget(self)
        self.table.doubleClicked.connect(self.table_mural_double)
        colunas = [{"Mensagem" : "", "Data" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents();
        self.table.setColumnCount(2);
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        header = self.table.horizontalHeader() 
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch);
        self.table.setRowCount(0)
        form_layout.addWidget(self.table);

        self.btn_novo = QPushButton("Novo item")
        self.btn_novo.clicked.connect(self.btn_novo_click); 
        form_layout.addWidget( self.btn_novo );

        self.setLayout(form_layout);

    def atualizar_tela(self):
        self.xmpp_var.adicionar_mensagem( "comandos.mural" ,"MuralComando", "listar", {} );
    
    def atualizar_tabela(self):
        self.table.setRowCount( len( self.mensagens ) );
        for i in range(len(self.mensagens)):
            self.table.setItem( i, 0, QTableWidgetItem( self.mensagens[i].titulo ) );
            self.table.setItem( i, 1, QTableWidgetItem( self.mensagens[i].data ) );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "MuralComando" and conteudo_js["funcao"] == "listar":
            self.mensagens = [];
            for i in range(len( conteudo_js["lista"] )):
                mural = Mural();
                mural.fromJson( conteudo_js["lista"][i] );
                self.mensagens.append(mural);
            self.atualizar_tabela();
    
    def btn_novo_click(self):     
        f = FormMuralAdicionar( self.xmpp_var );
        f.exec();
        self.xmpp_var.adicionar_mensagem( "comandos.mural" ,"MuralComando", "listar", {} );
    def table_mural_double(self):
        row = self.table.currentRow();
        f = FormMuralVer(self.xmpp_var, self.mensagens[row]);
        f.exec();


