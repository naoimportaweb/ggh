import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *

from form.form_atividade_corrigir import FormAtividadeCorrigir;

class PainelCorrigir(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        form_layout = QVBoxLayout( self );
        self.correcoes = [];
        self.table = QTableWidget(self)
        self.table.doubleClicked.connect(self.table_correcao_double)
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
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "nao_corrigidas", {} );
    
    def atualizar_tabela(self):
        self.table.setRowCount( len( self.correcoes ) );
        for i in range(len(self.correcoes)):
            correcao = self.correcoes[i];
            #atc.*, atv.titulo, atv.instrucao_correcao, atv.instrucao, atv.pontos_maximo FROM
            self.table.setItem( i, 0, QTableWidgetItem( correcao["titulo"][0:30] ) );
            self.table.setItem( i, 1, QTableWidgetItem( correcao["resposta"][0:30] ) );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "AtividadeComando" and conteudo_js["funcao"] == "nao_corrigidas" and conteudo_js.get("lista") != None:
            self.correcoes = conteudo_js["lista"];
            self.atualizar_tabela();
            
    def table_correcao_double(self):
        row = self.table.currentRow();
        f = FormAtividadeCorrigir( self.xmpp_var, self.correcoes[row], self );
        f.exec();
        self.correcoes.pop(row);
        self.atualizar_tabela();

