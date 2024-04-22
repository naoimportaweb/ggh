

import time, base64, uuid, os, sys, json, traceback, threading;

#from PySide6.QtGui import *
from PySide6.QtWidgets import   QGridLayout,QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;
from api.fsseguro import FsSeguro
from form.ui.combobox import ComboBox;
from classes.atividade import Atividade;
from form.form_edit_atividade import FormEditarAtividade
from form.funcoes import Utilitario;

CACHE_CMB_NIVEL = 'painel_atividade.cmb_nivel';

class PainelAtividade(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.lista_atividade = [];
        form_layout = QVBoxLayout( self );
        widget_pesquisa = QWidget();
        self.cmb_nivel = ComboBox(self, CACHE_CMB_NIVEL, configuracao=self.xmpp_var.cliente.configuracao); # QComboBox(); 
        self.cmb_nivel.currentIndexChanged.connect(self.cmb_nivel_selected)
        form_pesquisa = QHBoxLayout( widget_pesquisa );
        form_pesquisa.addWidget( QLabel("Nível", self) );
        form_pesquisa.addWidget( self.cmb_nivel );
        self.b5 = QPushButton("Atualizar lista")
        self.b5.setGeometry(10,0,32,32)
        self.b5.clicked.connect( self.botao_listar_atividade_click )
        form_pesquisa.addWidget( self.b5 );
        form_pesquisa.addStretch();
        form_layout.addWidget(widget_pesquisa);

        self.table = Utilitario.widget_tabela(self, ["Título", "Nível", "Pontos", "Respostas", "Status"], 
            tamanhos=[QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents], double_click=self.table_atividade_double);
        form_layout.addWidget(self.table);
        if self.xmpp_var.cliente.posso_tag("atividade_criar"):
            self.b4 = QPushButton("Nova atividade")
            self.b4.setGeometry(10,0,32,32)
            self.b4.clicked.connect( self.botao_novo_atividade_click )
            Utilitario.widget_linha(self, form_layout, [self.b4], stretch_inicio=True );
        self.setLayout(form_layout);

    def table_atividade_double(self):
        self.ativo = False;
        f = FormEditarAtividade( self.xmpp_var.cliente, self.xmpp_var, self.table.get() );
        f.exec();
        self.ativo = True;
        #self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "listar", {} );

    def atualizar_atividade( self ):
        self.table.cleanList();
        for i in range(len(self.lista_atividade)):
            if self.lista_atividade[i].posicao_nivel <= self.cmb_nivel.getObject().posicao:
                #print(self.lista_atividade[i]);
                self.table.add( [ self.lista_atividade[i].titulo , 
                                  self.lista_atividade[i].nome_nivel, 
                                  str(self.lista_atividade[i].pontos_maximo), 
                                  str(len(self.lista_atividade[i].respostas)),
                                  self.lista_atividade[i].getStatus() ], self.lista_atividade[i] );

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "AtividadeComando" and (conteudo_js["funcao"] == "salvar" or
           conteudo_js["funcao"] == "criar" or conteudo_js["funcao"] == "atividade_aprovar_reprovar" or 
           conteudo_js["funcao"] == "associar_operacao" ):
            self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "listar", {} );
        elif conteudo_js["comando"] == "AtividadeComando" and conteudo_js["funcao"] == "listar" :
            self.lista_atividade = [];
            for buffer in conteudo_js["lista"]:
                buffer_Atividade = Atividade( );
                buffer_Atividade.fromJson( buffer );
                self.lista_atividade.append( buffer_Atividade );
            self.atualizar_atividade();
    
    def botao_listar_atividade_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "listar", {} );
    def parar_tela(self):
        return;
    def atualizar_tela(self):
        #self.b4.setEnabled(self.xmpp_var.cliente.posso_tag("atividade_criar"));
        self.cmb_nivel.addArrayObject(self.xmpp_var.grupo.niveis, "id", "nome");
        if len(self.lista_atividade) == 0:
            self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "listar", {} );
    
    def cmb_nivel_selected(self):
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "listar", {} );
    
    def botao_novo_atividade_click(self):
        atividade = Atividade();
        atividade.titulo = "Nova Atividade";
        atividade.id_nivel = self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id;
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "criar", atividade.toJson() );
