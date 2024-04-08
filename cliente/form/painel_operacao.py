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
        self.cmb_nivel = QComboBox(); 
        self.cmb_nivel.activated.connect(self.cmb_nivel_selected)
        self.table = QTableWidget(self)
        self.table.doubleClicked.connect(self.table_operacao_double)
        colunas = [{ "Sigla": "", "Nome" : "", "Nível" : "", "Data de início" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents();
        self.table.setColumnCount(4);
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        header = self.table.horizontalHeader() 
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch);
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setRowCount(0)
        form_layout.addWidget( self.cmb_nivel );
        form_layout.addWidget(self.table);
        if self.xmpp_var.cliente.posso_tag("operacao_criar"):
            self.btn_novo = QPushButton("Novo item")
            self.btn_novo.clicked.connect(self.btn_novo_click); 
            form_layout.addWidget( self.btn_novo );
        self.setLayout(form_layout);
    
    def cmb_nivel_selected(self):
        self.xmpp_var.adicionar_mensagem( "comandos.operacao" ,"OperacaoComando", "listar", { "id_nivel" : self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id } );
    
    def atualizar_tela(self):
        if self.cmb_nivel.count() == 0 and len(self.xmpp_var.grupo.niveis) > 0:
            for nivel in self.xmpp_var.grupo.niveis:
                self.cmb_nivel.addItem(nivel.nome);
            self.cmb_nivel.setCurrentIndex(0);
        self.xmpp_var.adicionar_mensagem( "comandos.operacao" ,"OperacaoComando", "listar", { "id_nivel" : self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id } );
        return;
    
    def atualizar_tabela(self):
        self.table.setRowCount( len( self.operacoes ) );
        for i in range(len(self.operacoes)):
            self.table.setItem( i, 0, QTableWidgetItem( self.operacoes[i].sigla ) );
            self.table.setItem( i, 1, QTableWidgetItem( self.operacoes[i].nome ) );
            self.table.setItem( i, 2, QTableWidgetItem( self.operacoes[i].nome_nivel ) );
            self.table.setItem( i, 3, QTableWidgetItem( self.operacoes[i].data_inicio ) );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "OperacaoComando" and conteudo_js["funcao"] == "listar":
            self.operacoes = [];
            for i in range(len( conteudo_js["lista"] )):
                operacao = Operacao();
                operacao.fromJson( conteudo_js["lista"][i] );
                self.operacoes.append(operacao);
            self.atualizar_tabela();
        elif conteudo_js["comando"] == "OperacaoComando" and conteudo_js["funcao"] == "novo":
            self.xmpp_var.adicionar_mensagem( "comandos.operacao" ,"OperacaoComando", "listar", { "id_nivel" : self.xmpp_var.grupo.niveis[0].id } );
    def btn_novo_click(self):     
        operacao = Operacao();
        numero = str(time.time());
        operacao.nome = "Nova operação Número: " + numero;
        operacao.sigla = "#OpNovo_" + numero;
        operacao.id_nivel = self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id;
        self.xmpp_var.adicionar_mensagem( "comandos.operacao" ,"OperacaoComando", "novo", operacao.toJson() );
    
    def table_operacao_double(self):
        row = self.table.currentRow();
        f = FormOperacaoAdicionar(self.xmpp_var, self.operacoes[row]);
        f.exec();


