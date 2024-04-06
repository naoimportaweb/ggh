import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import    QGridLayout,QTextEdit, QTabWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from api.chachahelp import ChaChaHelper;
from api.SteganoHelper import SteganoHelper;

class PainelConta(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        self.main_layout = QVBoxLayout( self );
        tab = QTabWidget();  
        self.main_layout.addWidget(tab);   
        
        page_dados = QWidget(tab);
        page_dados_layout = QVBoxLayout();
        page_dados.setLayout(page_dados_layout);
        tab.addTab(page_dados,'Dados');
        self.layout_dados( page_dados_layout );

        page_login = QWidget(tab);
        page_login_layout = QVBoxLayout();
        page_login.setLayout(page_login_layout);
        tab.addTab(page_login,'Autenticação');
        self.layout_login( page_login_layout );

        page_tags = QWidget(tab);
        page_tags_layout = QVBoxLayout();
        page_tags.setLayout(page_tags_layout);
        tab.addTab(page_tags,'TAGs');
        self.layout_tag( page_tags_layout );

        page_niveis = QWidget(tab);
        page_niveis_layout = QVBoxLayout();
        page_niveis.setLayout(page_niveis_layout);
        tab.addTab(page_niveis,'Níveis');
        self.layout_nivel( page_niveis_layout );

        self.setLayout(self.main_layout);

    def recarregar_tags(self):
        self.table.setRowCount(len(self.xmpp_var.cliente.tags));
        for i in range(len(self.xmpp_var.cliente.tags)):
            self.table.setItem( i, 0, QTableWidgetItem( self.xmpp_var.cliente.tags[i]["sigla"] ) );
            self.table.setItem( i, 1, QTableWidgetItem( self.xmpp_var.cliente.tags[i]["nome"] ) );
    
    def recarregar_niveis(self):
        adicionado = 0;
        for i in range(len(self.xmpp_var.grupo.niveis)):
            if self.xmpp_var.grupo.niveis[i].posicao <= self.xmpp_var.cliente.nivel_posicao:
                self.table1.setRowCount(adicionado + 1);
                self.table1.setItem( adicionado, 0, QTableWidgetItem( self.xmpp_var.grupo.niveis[i].nome ) );
                adicionado = adicionado + 1;

    def atualizar_tela(self):
        if self.layout_carregado:
            return;
        if self.xmpp_var.cliente.tags == None:
            return;
        self.recarregar_niveis();
        self.recarregar_tags();
        self.layout_carregado = True;


    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ClienteCadastroComando" and conteudo_js["funcao"] == "alterar_nome":
            self.lb_apelido.setText( self.xmpp_var.cliente.apelido );
        elif conteudo_js["comando"] == "ClienteCadastroComando" and conteudo_js["funcao"] == "atualizar_tags":
            self.recarregar_tags();
    
    def layout_tag(self, layout):
        widget = QWidget(self);
        widget_layout = QHBoxLayout();
        widget.setLayout(widget_layout);
        widget_layout.addStretch();
        btn_atualizar_tag = QPushButton("Atualizar as TAGs")
        btn_atualizar_tag.clicked.connect(self.btn_atualizar_tag_click); 
        widget_layout.addWidget( btn_atualizar_tag );
        layout.addWidget(widget);

        self.table = QTableWidget(self)
        colunas = [{"sigla" : "", "Título" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents();
        self.table.setColumnCount(2);
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        header = self.table.horizontalHeader() 
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch);
        layout.addWidget(self.table);

    def layout_nivel(self, layout):
        self.table1 = QTableWidget(self)
        colunas = [{"Nome" : ""}];
        self.table1.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table1.resizeColumnsToContents();
        self.table1.setColumnCount(1);
        self.table1.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.table1.setHorizontalHeaderLabels(colunas[0].keys());
        header = self.table1.horizontalHeader() 
        header.setSectionResizeMode(0, QHeaderView.Stretch);
        layout.addWidget(self.table1);
    
    def layout_dados(self, layout):
        widget = QWidget(self);
        widget_layout = QHBoxLayout();
        widget.setLayout(widget_layout);
        widget_layout.addWidget(QLabel("Apelido", self));
        self.lb_apelido = QLabel("<b>" + self.xmpp_var.cliente.apelido + "</b>", self );
        widget_layout.addWidget(self.lb_apelido);
        btn_rename = QPushButton("Gerar novo apelido")
        btn_rename.clicked.connect(self.widget_layout_click); 
        widget_layout.addWidget( btn_rename );
        widget_layout.addStretch();
        layout.addWidget(widget);
        layout.addStretch();

    def widget_layout_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.cliente_cadastro" ,"ClienteCadastroComando", "alterar_nome", {});
        return;

    def layout_login(self, layout):
        btn_gerar_imagem = QPushButton("Gerar arquivo chave (exportar)")
        btn_gerar_imagem.clicked.connect(self.btn_gerar_imagem_click); 
        layout.addWidget( btn_gerar_imagem );
    
    def btn_atualizar_tag_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.cliente_cadastro" ,"ClienteCadastroComando", "atualizar_tags", {});

    def btn_gerar_imagem_click(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        path_arquivo = folder_path + "/chave.gif";
        self.xmpp_var.cliente.fs.escrever_json(path_arquivo, self.xmpp_var.cliente.toJson());
        QMessageBox.information(self, "Arquivo criado", "O arquivo foi salvo, o path é:\n" + path_arquivo, QMessageBox.StandardButton.Ok);
