import sys, os, json, base64, re, requests;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import *
from PySide6 import QtWidgets;
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from form.form_atividade_resposta import FormAtividadeResposta

class FormEditarAtividade(QDialog):
    def __init__(self, cliente, xmpp_var, atividade, parent=None):
        super(FormEditarAtividade, self).__init__(parent);
        self.cliente = cliente;
        self.xmpp_var = xmpp_var;
        self.atividade = atividade;
        self.setWindowTitle("Atividade");
        self.setGeometry(400, 400, 800, 500);
        self.main_layout = QVBoxLayout( self );
        self.textEditAtividade = None;
        self.table = None;

        tab =       QTabWidget();        
        self.main_layout.addWidget(tab);

        if atividade.id_cliente == self.cliente.id:# and self.xmpp_var.cliente.posso_tag("atividade_criar"):
            self.widget_botton = QWidget();
            self.botton_layout = QHBoxLayout();
            self.widget_botton.setLayout( self.botton_layout );
            self.btn_salvar = QPushButton("Salvar")
            self.btn_salvar.clicked.connect(self.btn_click_salvar); 
            self.botton_layout.addStretch();
            self.botton_layout.addWidget( self.btn_salvar );
            self.main_layout.addWidget(self.widget_botton);

        page_atividade = QWidget(tab);
        page_atividade_layout = QVBoxLayout();
        page_atividade.setLayout(page_atividade_layout);
        tab.addTab(page_atividade,'Atividade');

        page_respostas = QWidget(tab);
        page_respostas_layout = QGridLayout();
        page_respostas.setLayout(page_respostas_layout);
        tab.addTab(page_respostas,'Respostas');

        self.layout_resposta( page_respostas_layout ,       self.atividade);
        self.layout_atividade( page_atividade_layout,       self.atividade);
        self.showMaximized() 

    def layout_atividade(self, layout, atividade):
        layout.addWidget( QLabel("Atividade", self) );
        self.titulo = QLineEdit(self);
        layout.addWidget( self.titulo );
        self.titulo.setText( self.atividade.titulo );

        self.textEditAtividade = QTextEdit(self);
        self.textEditAtividade.setPlainText( atividade.atividade );
        layout.addWidget( self.textEditAtividade );
    
    def layout_resposta(self, layout, atividade):
        layout.addWidget( QLabel("Repostas", self) );
        self.table = QTableWidget(self)
        colunas = [{"Título" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        self.table.setRowCount(0)
        layout.addWidget(self.table);
        self.table.setRowCount( len(  self.atividade.respostas  ) );
        index = 0;
        for resposta in self.atividade.respostas:
            self.table.setItem( index, 0, QTableWidgetItem( resposta.data ) );
            index = index + 1;
        widget_botton_resposta = QWidget();
        botton_layout_resposta = QHBoxLayout();
        widget_botton_resposta.setLayout(    botton_layout_resposta );
        btn_salvar_resposta = QPushButton("Responder")
        btn_salvar_resposta.clicked.connect( self.btn_click_salvar_resposta); 
        botton_layout_resposta.addStretch();
        botton_layout_resposta.addWidget(    btn_salvar_resposta );
        layout.addWidget( widget_botton_resposta );
    
    def btn_click_salvar_resposta(self):
        f = FormAtividadeResposta(self.xmpp_var, self.atividade, index_resposta=None, parent=self );
        f.exec();
    
    def btn_click_salvar(self):
        self.atividade.atividade = self.textEditAtividade.toPlainText();
        self.atividade.titulo = self.titulo.text();
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "salvar", self.atividade.toJson() );
