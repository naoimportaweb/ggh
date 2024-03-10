

import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *
from api.fsseguro import FsSeguro

from classes.atividade import Atividade;
from form.form_edit_atividade import FormEditarAtividade

class PainelAtividade(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.lista_atividade = [];
        form_layout = QVBoxLayout( self );
        widget_pesquisa = QWidget();
        self.cmb_nivel = QComboBox(); 
        form_pesquisa = QHBoxLayout( widget_pesquisa );
        form_pesquisa.addWidget( QLabel("Nível", self) );
        form_pesquisa.addWidget( self.cmb_nivel );
        form_pesquisa.addStretch();
        self.b5 = QPushButton("Atualizar lista")
        self.b5.setGeometry(10,0,32,32)
        self.b5.clicked.connect( self.botao_listar_atividade_click )
        form_pesquisa.addWidget( self.b5 );
        form_layout.addWidget(widget_pesquisa);

        #https://www.pythontutorial.net/pyqt/pyqt-qtablewidget/
        self.table = QTableWidget(self)
        colunas = [{"Título" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        self.table.setRowCount(0)
        form_layout.addWidget(self.table);
        
        widget_acesso = QWidget();
        form_acesso = QHBoxLayout( widget_acesso );
        
        self.b6 = QPushButton("Acessar atividade")
        self.b6.setGeometry(10,0,32,32)
        self.b6.clicked.connect( self.botao_acessar_atividade_click )
        form_acesso.addWidget( self.b6 );
        form_acesso.addStretch();

        if self.xmpp_var.cliente.posso_tag("atividade_criar"):
            self.b4 = QPushButton("Nova atividade")
            self.b4.setGeometry(10,0,32,32)
            self.b4.clicked.connect( self.botao_novo_atividade_click )
            form_acesso.addWidget( self.b4 );

        form_layout.addWidget(widget_acesso);
        self.setLayout(form_layout);

        self.thread_enviador = threading.Thread(target = self.atualizar_atividade, args=());
        self.thread_enviador.start();
    
    def atualizar_atividade( self ):
        while True:
            try:
                if self.cmb_nivel.currentIndex() >= 0 and self.ativo:
                    lista_buffer = os.listdir(  self.xmpp_var.cliente.path_atividade  );
                    for buffer_nome_atividade in lista_buffer:
                        buffer_Atividade = Atividade( );
                        buffer_Atividade.carregar( self.xmpp_var.cliente.chave_local, self.xmpp_var.cliente.path_atividade + "/" + buffer_nome_atividade );
                        if len([x for x in self.lista_atividade if x.id == buffer_Atividade.id]) == 0:
                            self.lista_atividade.append( buffer_Atividade );
                            self.table.setRowCount( len(  self.lista_atividade  ) );
                            self.table.setItem( len(self.lista_atividade) - 1, 0, QTableWidgetItem( buffer_Atividade.titulo ) );
                            self.table.setItem( len(self.lista_atividade) - 1, 1, QTableWidgetItem("") );
            except:
                traceback.print_exc();
            time.sleep(5);
            self.table.resizeColumnsToContents();

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ConhecimentoAtividade" and conteudo_js["funcao"] == "listar":
            print("Carregou.");
    
    def botao_listar_atividade_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "listar", {} );

    def atualizar_tela(self):
        self.cmb_nivel.clear();
        if len(self.xmpp_var.grupo.niveis) > 0:
            for nivel in self.xmpp_var.grupo.niveis:
                self.cmb_nivel.addItem(nivel.nome);
            self.cmb_nivel.setCurrentIndex(0);
            self.botao_listar_atividade_click();
    
    def botao_acessar_atividade_click(self):
        row = self.table.currentRow();
        f = FormEditarAtividade( self.xmpp_var.cliente, self.xmpp_var, self.lista_atividade[ row ] );
        f.exec();
        #self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "carregar", {"id" : self.lista_atividade[row]["id"] } );
    
    def botao_novo_atividade_click(self):
        atividade = Atividade();
        atividade.titulo = "Nova Atividade";
        atividade.id_nivel = self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id;
        print("Atividade: ", atividade);
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "criar", atividade.toJson() );
