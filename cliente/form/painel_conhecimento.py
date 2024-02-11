

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
        colunas = [{"Autor": "", "Título" : "", "Status" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        self.table.setRowCount(0)
        form_layout.addWidget(self.table);
        
        self.b4 = QPushButton("Novo conhecimento")
        self.b4.setGeometry(10,0,32,32)
        self.b4.clicked.connect( self.botao_novo_conhecimento_click )
        form_layout.addWidget( self.b4 );
        self.setLayout(form_layout);
        

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "ConhecimentoComando" and conteudo_js["funcao"] == "listar":
            self.table.clearContents();
            self.table.setRowCount(len(conteudo_js['lista']))
            row = 0
            for conhecimento in conteudo_js['lista']:
                self.table.setItem(row, 0, QTableWidgetItem(conhecimento['apelido']))
                self.table.setItem(row, 1, QTableWidgetItem(conhecimento['titulo']))
                if conhecimento['status'] == 0:
                    self.table.setItem(row, 2, QTableWidgetItem("Em edição"))
                elif conhecimento['status'] == 1:
                    self.table.setItem(row, 2, QTableWidgetItem("Aguardando aprovação"))
                if conhecimento['status'] == 2:
                    self.table.setItem(row, 2, QTableWidgetItem("Aprovado"))
                row += 1
            self.table.resizeColumnsToContents()
        elif conteudo_js["comando"] == "ConhecimentoComando" and conteudo_js["funcao"] == "salvar":
            # dizer que salvou
            print("SALVAR:", conteudo_js);
        elif conteudo_js["comando"] == "ConhecimentoComando" and conteudo_js["funcao"] == "aprovar":
            # dizer que aprovou e mudar o layout
            print("APROVAR:", conteudo_js);
        elif conteudo_js["comando"] == "ConhecimentoComando" and ( conteudo_js["funcao"] == "carregar" or conteudo_js["funcao"] == "novo" ):
            conhecimento = Conhecimento();
            conhecimento.fromJson( js["conhecimento"] );
            f = FormEditarConhecimento( self.xmpp_var.cliente, self.xmpp_var.grupo, conhecimento );
            f.exec();
    def botao_listar_conhecimento_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "listar", {"id_nivel" : self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ]["id"] } );

    def atualizar_tela(self):
        self.cmb_nivel.clear();
        if len(self.xmpp_var.grupo.niveis) > 0:
            for nivel in self.xmpp_var.grupo.niveis:
                self.cmb_nivel.addItem(nivel["nome"]);
            self.cmb_nivel.setCurrentIndex(0);
            self.botao_listar_conhecimento_click();
    
    def botao_novo_conhecimento_click(self):
        conhecimento = Conhecimento();
        conhecimento.titulo = "Novo conhecimento";
        conhecimento.id_cliente = self.xmpp_var.cliente.id;
        conhecimento.id_nivel = self.xmpp_var.grupo.niveis[ self.xmpp_var.cliente.nivel_posicao ]["id"];
        self.xmpp_var.adicionar_mensagem( "comandos.conhecimento" ,"ConhecimentoComando", "novo", conhecimento.toJson() );