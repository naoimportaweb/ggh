

import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *
from api.fsseguro import FsSeguro

from classes.conhecimento import Conhecimento;
from form.form_edit_conhecimento import FormEditarConhecimento

class PainelConhecimento(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.lista_conhecimento = [];
        form_layout = QVBoxLayout( self );
        widget_pesquisa = QWidget();
        self.cmb_nivel = QComboBox(); 
        form_pesquisa = QHBoxLayout( widget_pesquisa );
        form_pesquisa.addWidget( QLabel("Nível", self) );
        form_pesquisa.addWidget( self.cmb_nivel );
        form_pesquisa.addStretch();
        self.b5 = QPushButton("Atualizar lista")
        self.b5.setGeometry(10,0,32,32)
        self.b5.clicked.connect( self.botao_listar_conhecimento_click )
        form_pesquisa.addWidget( self.b5 );
        form_layout.addWidget(widget_pesquisa);

        #https://www.pythontutorial.net/pyqt/pyqt-qtablewidget/
        self.table = QTableWidget(self)
        colunas = [{"Título" : "", "Status" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        self.table.setRowCount(0)
        form_layout.addWidget(self.table);
        
        widget_acesso = QWidget();
        form_acesso = QHBoxLayout( widget_acesso );
        
        self.b6 = QPushButton("Acessar conhecimento")
        self.b6.setGeometry(10,0,32,32)
        self.b6.clicked.connect( self.botao_acessar_conhecimento_click )
        form_acesso.addWidget( self.b6 );
        form_acesso.addStretch();

        self.b4 = QPushButton("Novo conhecimento")
        self.b4.setGeometry(10,0,32,32)
        self.b4.clicked.connect( self.botao_novo_conhecimento_click )
        form_acesso.addWidget( self.b4 );

        form_layout.addWidget(widget_acesso);
        self.setLayout(form_layout);

        self.thread_enviador = threading.Thread(target = self.atualizar_conhecimento, args=());
        self.thread_enviador.start();
    
    def atualizar_conhecimento( self ):
        while True:
            try:
                if self.cmb_nivel.currentIndex() >= 0 and self.ativo:
                    lista_buffer = os.listdir(  self.xmpp_var.cliente.path_conhecimento  );
                    for buffer_nome_conhecimento in lista_buffer:
                        buffer_conhecimento = Conhecimento( );
                        buffer_conhecimento.carregar( self.xmpp_var.cliente.chave_local, self.xmpp_var.cliente.path_conhecimento + "/" + buffer_nome_conhecimento );
                        if len([x for x in self.lista_conhecimento if x.id == buffer_conhecimento.id]) == 0:
                            self.lista_conhecimento.append( buffer_conhecimento );
                            self.table.setRowCount( len(  self.lista_conhecimento  ) );
                            self.table.setItem( len(self.lista_conhecimento) - 1, 0, QTableWidgetItem( buffer_conhecimento.titulo ) );
                            self.table.setItem( len(self.lista_conhecimento) - 1, 1, QTableWidgetItem("") );
            except:
                traceback.print_exc();
            time.sleep(5);
            self.table.resizeColumnsToContents();

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ConhecimentoComando" and conteudo_js["funcao"] == "listar":
            for conhecimento in conteudo_js['lista']:
                buffer = Conhecimento(  );
                buffer.fromJson( conhecimento );
                buffer.salvar( self.xmpp_var.cliente.chave_local, self.xmpp_var.cliente.path_conhecimento );

        elif conteudo_js["comando"] == "ConhecimentoComando" and conteudo_js["funcao"] == "salvar":
            buffer = Conhecimento(  );
            buffer.fromJson( conteudo_js["conhecimento"] );
            buffer.salvar( self.xmpp_var.cliente.chave_local, self.xmpp_var.cliente.path_conhecimento );
            index = -1;
            for i in range(len(self.lista_conhecimento)):
                if self.lista_conhecimento[i].id == buffer.id:
                    index = i;
                    break;
            if index >= 0:
                self.lista_conhecimento[i] = buffer;
                self.table.setItem( index, 0, QTableWidgetItem( buffer.titulo ) );
    
    def botao_listar_conhecimento_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "listar", {"id_nivel" : self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id } );

    def atualizar_tela(self):
        self.cmb_nivel.clear();
        if len(self.xmpp_var.grupo.niveis) > 0:
            for nivel in self.xmpp_var.grupo.niveis:
                self.cmb_nivel.addItem(nivel.nome);
            self.cmb_nivel.setCurrentIndex(0);
            self.botao_listar_conhecimento_click();
    
    def botao_acessar_conhecimento_click(self):
        row = self.table.currentRow();
        f = FormEditarConhecimento( self.xmpp_var.cliente, self.xmpp_var, self.lista_conhecimento[ row ] );
        f.exec();
        #self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "carregar", {"id" : self.lista_conhecimento[row]["id"] } );
    
    def botao_novo_conhecimento_click(self):
        conhecimento = Conhecimento();
        conhecimento.titulo = "Novo conhecimento";
        conhecimento.id_cliente = self.xmpp_var.cliente.id;
        conhecimento.id_nivel = self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id;
        self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "novo", conhecimento.toJson() );
        #self.lista_conhecimento = [];
        #self.table.clearContents();