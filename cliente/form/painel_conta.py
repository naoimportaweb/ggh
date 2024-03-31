import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *

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
        tab.addTab(page_dados,'Reposta');
        self.layout_dados( page_dados_layout );

        self.setLayout(self.main_layout);

    def atualizar_tela(self):
        if self.layout_carregado:
            return;
        self.layout_carregado = True;

    def evento_mensagem(self, de, texto, message, conteudo_js):
        print();

    def layout_dados(self, layout):
        print();

