import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import    QGridLayout,QTextEdit, QTabWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from api.chachahelp import ChaChaHelper;
from api.SteganoHelper import SteganoHelper;
from form.funcoes import Utilitario;

class PainelConta(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.main_layout = QVBoxLayout( self );
        tab = QTabWidget();  
        self.main_layout.addWidget(tab);   
        
        page_dados_layout = Utilitario.widget_tab(tab, "Dados");
        self.layout_dados( page_dados_layout );
        page_login_layout = Utilitario.widget_tab(tab, "Autenticação")
        self.layout_login( page_login_layout );
        page_tags_layout = Utilitario.widget_tab(tab, "TAGs")
        self.layout_tag( page_tags_layout );
        page_niveis_layout = Utilitario.widget_tab(tab, "Níveis")
        self.layout_nivel( page_niveis_layout );

        self.setLayout(self.main_layout);

    def recarregar_tags(self):
        if self.xmpp_var.cliente.tags == None:
            return;
        self.table.setRowCount(len(self.xmpp_var.cliente.tags));
        for i in range(len(self.xmpp_var.cliente.tags)):
            self.table.setItem( i, 0, QTableWidgetItem( self.xmpp_var.cliente.tags[i]["sigla"] ) );
            self.table.setItem( i, 1, QTableWidgetItem( self.xmpp_var.cliente.tags[i]["nome"] ) );
    
    def recarregar_niveis(self):
        if self.xmpp_var.grupo.niveis == None:
            return;
        self.table1.cleanList();
        for i in range(len(self.xmpp_var.grupo.niveis)):
            if self.xmpp_var.grupo.niveis[i].posicao <= self.xmpp_var.cliente.nivel_posicao:
                self.table1.add( [self.xmpp_var.grupo.niveis[i].nome,
                                  str(self.xmpp_var.grupo.niveis[i].posicao),
                                  str(self.xmpp_var.grupo.niveis[i].pontuacao),
                                  str(self.xmpp_var.grupo.niveis[i].tempo) ], self.xmpp_var.grupo.niveis[i] );
    def parar_tela(self):
        return;
    def atualizar_tela(self):
        self.recarregar_niveis();
        self.recarregar_tags();

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ClienteCadastroComando" and conteudo_js["funcao"] == "alterar_nome":
            self.lb_apelido.setText( "<b>" + self.xmpp_var.cliente.apelido + "</b>" );
        elif conteudo_js["comando"] == "ClienteCadastroComando" and conteudo_js["funcao"] == "atualizar_tags":
            self.recarregar_tags();
    
    def layout_tag(self, layout):
        btn_atualizar_tag = QPushButton("Atualizar as TAGs")
        btn_atualizar_tag.clicked.connect(self.btn_atualizar_tag_click); 
        Utilitario.widget_linha(self, layout, [btn_atualizar_tag], stretch_inicio=True );
        self.table = Utilitario.widget_tabela(self, ["Sigla", "Título"], tamanhos=[QHeaderView.ResizeToContents, QHeaderView.Stretch]);
        layout.addWidget(self.table);


    def layout_nivel(self, layout):
        self.table1 = Utilitario.widget_tabela(self, ["Nome", "Posicao", "Pontos", "Tempo"], [QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents]);
        layout.addWidget(self.table1);
    
    def layout_dados(self, layout):
        lb_label_buffer = QLabel("Apelido: ", self);
        self.lb_apelido = QLabel("<b>" + self.xmpp_var.cliente.apelido + "</b>", self );
        btn_rename = QPushButton("Gerar novo apelido")
        btn_rename.clicked.connect(self.widget_layout_click); 
        Utilitario.widget_linha(self, layout, [ lb_label_buffer, self.lb_apelido, btn_rename ], stretch_fim=True);
        btn_logoff = QPushButton("Logoff")
        btn_logoff.clicked.connect(self.btn_logoff_click); 
        Utilitario.widget_linha(self, layout, [ btn_logoff ], stretch_fim=True);
        layout.addStretch();
    
    def btn_logoff_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.cliente_cadastro" ,"ClienteCadastroComando", "logoff", {});
    
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
