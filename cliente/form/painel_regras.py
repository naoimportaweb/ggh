import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;
from PySide6.QtWidgets import  QGridLayout, QTextEdit, QTextBrowser, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6 import QtWidgets;
from PySide6.QtCore import Qt, QObject
from PySide6.QtCore import  QFileSystemWatcher, QSettings, Signal, Slot, QThread;
from api.fsseguro import FsSeguro

class PainelRegras(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.fs = FsSeguro( self.xmpp_var.cliente.chave_local );
        self.path_html = self.xmpp_var.grupo.path_grupo_html + "/regras.html";
        self.layout_carregado = False;
        
    def botao_editar_click(self):
        self.xmpp_var.adicionar_mensagem( "comandos.html" ,"HtmlComando", "post",
                                          {"path" : "regras.html", "html" : self.txt_texto.toHtml() } );
    def atualizar_tela(self):
        if self.layout_carregado:
            return;
        form_layout = QVBoxLayout( self );
        html = self.fs.ler_raw( self.path_html );
        if self.xmpp_var.cliente.posso_tag("recomendacao_editar"):
            self.txt_texto = QTextEdit(self);
            palette = QPalette()
            palette.setColor(QPalette.WindowText, Qt.black);
            palette.setColor(QPalette.Text, Qt.black);
            self.txt_texto.setPalette(palette);
            self.txt_texto.setStyleSheet("background-color: rgb(255, 255, 255);");
            self.txt_texto.setHtml( html );
            form_layout.addWidget( self.txt_texto );

            b4_widget = QWidget( self );
            b4_layout = QHBoxLayout();
            b4_widget.setLayout(b4_layout);
            b4 = QPushButton("Editar Regras")
            b4.clicked.connect( self.botao_editar_click )
            b4_layout.addStretch();
            b4_layout.addWidget( b4 );
            form_layout.addWidget( b4_widget );
        else:
            self.tb = QTextBrowser(self);
            palette = QPalette()
            palette.setColor(QPalette.WindowText, Qt.black);
            palette.setColor(QPalette.Text, Qt.black);
            self.tb.setPalette(palette);
            self.tb.setStyleSheet("background-color: rgb(255, 255, 255);");
            self.tb.setAcceptRichText(True);
            self.tb.setOpenExternalLinks(False);
            self.tb.setHtml(self.fs.ler_raw( self.path_html ));
            form_layout.addWidget( self.tb );
            self.tb.setHtml(html);
        
        self.setLayout(form_layout);
        self.layout_carregado = True;

    def evento_mensagem(self, de, texto, message, conteudo_js):
        return;