import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *

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
        tab.addTab(page_login,'Dados');
        self.layout_login( page_login_layout );

        self.setLayout(self.main_layout);

    def atualizar_tela(self):
        if self.layout_carregado:
            return;
        self.layout_carregado = True;

    def evento_mensagem(self, de, texto, message, conteudo_js):
        print();

    def layout_dados(self, layout):
        print();
    def layout_login(self, layout):
        btn_gerar_imagem = QPushButton("Responder")
        btn_gerar_imagem.clicked.connect(self.btn_gerar_imagem_click); 
        layout.addWidget( btn_gerar_imagem );
    def btn_gerar_imagem_click(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.xmpp_var.cliente.fs.escrever_json(folder_path + "/chave.txt", self.xmpp_var.cliente.toJson());
        #dialog = QFileDialog(self)
        #dialog.setDirectory('/')
        #dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        #dialog.setNameFilter("Image (*.gif *.jpg *.png)")
        #dialog.setViewMode(QFileDialog.ViewMode.List)
        #if dialog.exec():
        #    filenames = dialog.selectedFiles();
        #    if filenames:
        #        self.xmpp_var.cliente.fs.escrever_json("/tmp/chave.txt", self.xmpp_var.cliente.toJson());
        #        #chacha = ChaChaHelper(self.xmpp_var.cliente.chave_local);
        #        #print( "Cliente: ", json.dumps(self.xmpp_var.cliente.toJson()) );
        #        #stg = SteganoHelper(chacha);
        #        #stg.encode(filenames[0], "um texto idiota.");
        #        #print("Foi obtido da imagem: ", stg.decode("/tmp/hacker_stegano_.png"));
