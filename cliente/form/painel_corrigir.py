import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *

class PainelCorrigir(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        form_layout = QVBoxLayout( self );
        
        self.table = QTableWidget(self)
        #self.table.doubleClicked.connect(self.table_corrigir_double)
        colunas = [{"Atividade" : "", "Resposta" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents();
        self.table.setColumnCount(2);
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        header = self.table.horizontalHeader() 
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch);
        self.table.setRowCount(0)
        form_layout.addWidget(self.table);
        self.setLayout(form_layout);

    def atualizar_tela(self):
        if self.layout_carregado:
            return;
        self.layout_carregado = True;
    
    def evento_mensagem(self, de, texto, message, conteudo_js):
        print();