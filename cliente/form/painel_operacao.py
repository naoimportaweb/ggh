import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import  QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from classes.operacao import Operacao;
from form.form_operacao_adicionar import FormOperacaoAdicionar;

class PainelOperacao(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        form_layout = QVBoxLayout( self );
        self.operacoes = [];
        self.table = QTableWidget(self)
        self.table.doubleClicked.connect(self.table_operacao_double)
        colunas = [{"nome" : "", "data_inicio" : ""}];
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
        self.xmpp_var.adicionar_mensagem( "comandos.operacao" ,"OperacaoComando", "listar", {} );
    
    def atualizar_tabela(self):
        self.table.setRowCount( len( self.operacoes ) );
        for i in range(len(self.operacoes)):
            self.table.setItem( i, 0, QTableWidgetItem( self.operacoes[i].titulo ) );
            self.table.setItem( i, 1, QTableWidgetItem( self.operacoes[i].data_inicio ) );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "OperacaoComando" and conteudo_js["funcao"] == "listar":
            self.operacoes = [];
            for i in range(len( conteudo_js["lista"] )):
                operacao = Operacao();
                operacao.fromJson( conteudo_js["lista"][i] );
                self.operacoes.append(operacao);
            self.atualizar_tabela();
    
    def btn_novo_click(self):     
        operacao = Operacao();
        operacao.id = "1";
        operacao.nome = "aaaa"
        operacao.sigla = "#OpAaaa"
        operacao.data_inicio = "2024-01-01 00:00:01"
        operacao.data_fim = "2024-01-01 00:00:01"


        self.operacoes.append( operacao );
        f = FormOperacaoAdicionar( self.xmpp_var, operacao );
        f.exec();
        self.xmpp_var.adicionar_mensagem( "comandos.operacao" ,"OperacaoComando", "listar", {} );
    
    def table_operacao_double(self):
        row = self.table.currentRow();
        f = FormOperacaoAdicionar(self.xmpp_var, self.operacoes[row]);
        f.exec();


