

import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtWidgets import  QGridLayout,QTextEdit,  QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
#from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;
from api.fsseguro import FsSeguro

from classes.conexao.monitor_request import MonitorRequest;
from classes.conhecimento import Conhecimento;
from form.form_edit_conhecimento import FormEditarConhecimento
from form.ui.combobox import ComboBox;
from form.funcoes import Utilitario;

CACHE_CMB_NIVEL = 'painel_conhecimento.cmb_nivel';

class PainelConhecimento(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.lista_conhecimento = [];
        form_layout = QVBoxLayout( self );
        widget_pesquisa = QWidget();
        self.cmb_nivel = ComboBox(self, CACHE_CMB_NIVEL, configuracao=self.xmpp_var.cliente.configuracao);
        self.cmb_nivel.currentIndexChanged.connect(self.botao_listar_conhecimento_click); # mesmo evento do botao de atualizar
        form_pesquisa = QHBoxLayout( widget_pesquisa );
        form_pesquisa.addWidget( QLabel("Nível", self) );
        form_pesquisa.addWidget( self.cmb_nivel );
        self.b5 = QPushButton("Atualizar lista")
        self.b5.setGeometry(10,0,32,32)
        self.b5.clicked.connect( self.botao_listar_conhecimento_click )
        form_pesquisa.addWidget( self.b5 );
        form_pesquisa.addStretch();
        form_layout.addWidget(widget_pesquisa);

        self.table = Utilitario.widget_tabela(self, ["Título", "Status"], [QHeaderView.Stretch, QHeaderView.ResizeToContents ], double_click=self.table_conhecimento_double)
        form_layout.addWidget(self.table);
        
        widget_acesso = QWidget();
        form_acesso = QHBoxLayout( widget_acesso );
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
                            self.table.setItem( len(self.lista_conhecimento) - 1, 1, QTableWidgetItem( buffer_conhecimento.nome_status ) );
            except:
                traceback.print_exc();
            time.sleep(5);

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
        self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "listar", 
            {"id_nivel" : self.cmb_nivel.getSelected().key } );
    def parar_tela(self):
        return;
    def atualizar_tela(self):
        self.cmb_nivel.addArrayObject(self.xmpp_var.grupo.niveis, "id", "nome");
        self.botao_listar_conhecimento_click(); # listar 
    
    #def botao_acessar_conhecimento_click(self):
    def table_conhecimento_double(self):
        row = self.table.currentRow();
        f = FormEditarConhecimento( self.xmpp_var.cliente, self.xmpp_var, self.lista_conhecimento[ row ] );
        f.exec();
    
    def callback_novo_item(self, mensagem):
        try:
            self.ativo = False;
            buffer = Conhecimento(  );
            buffer.fromJson( mensagem.toJson()["conhecimento"] );
            f = FormEditarConhecimento( self.xmpp_var.cliente, self.xmpp_var, buffer );
            f.exec();
            self.thread_aguardar.quit();
            self.thread_aguardar = None;
            self.ativo = True;
        except:
            traceback.print_exc();
        finally:
            self.b4.setDisabled(False);
    def botao_novo_conhecimento_click(self):
        try:
            conhecimento = Conhecimento();
            conhecimento.titulo = "Novo conhecimento";
            conhecimento.id_cliente = self.xmpp_var.cliente.id;
            conhecimento.id_nivel = self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id;
            request_id = self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "novo", conhecimento.toJson() );
            self.thread_aguardar = MonitorRequest(request_id, self.xmpp_var, self.callback_novo_item);
        except:
            traceback.print_exc();
        finally:
            self.b4.setDisabled(True);            