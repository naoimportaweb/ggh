import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import   QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from form.form_atividade_corrigir import FormAtividadeCorrigir;
from form.funcoes import Utilitario;

class PainelCorrigir(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        #self.layout_carregado = False;
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
        btn = QPushButton("Atualizar")
        btn.clicked.connect(self.btn_click);
        Utilitario.widget_linha(self, form_layout, [btn], stretch_fim=True);
        form_layout.addWidget(self.table);
        self.setLayout(form_layout);
    
    def btn_click(self):
        self.correcoes = [];
        self.atualizar_tela();
    def parar_tela(self):
        return;
    def atualizar_tela(self):
        if len(self.correcoes) > 0:
            return;
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "nao_corrigidas", {} );
    
    def atualizar_tabela(self):
        self.table.setRowCount( len( self.correcoes ) );
        for i in range(len(self.correcoes)):
            correcao = self.correcoes[i];
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

