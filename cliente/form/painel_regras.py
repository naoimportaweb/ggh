import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QScrollArea, QFrame, QMessageBox, QPlainTextEdit, QLabel, QListWidget, QListWidgetItem, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QHBoxLayout, QVBoxLayout, QMenuBar, QTextBrowser;
from PySide6.QtWidgets import QSizePolicy, QSizePolicy;
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
        self.path_regra = self.xmpp_var.grupo.path_grupo_html + "/regras.html";
        form_layout = QVBoxLayout( self );
        self.tb = QTextBrowser(self);
        self.tb.setAcceptRichText(True);
        self.tb.setOpenExternalLinks(False);
        self.tb.setHtml(self.fs.ler_raw( self.path_regra ));
        self.b4 = QPushButton("Atualizar")
        self.b4.setGeometry(10,0,32,32)
        self.b4.clicked.connect( self.botao_atualizar_click )
        form_layout.addWidget( self.tb );
        form_layout.addWidget( self.b4 );
        form_layout.addStretch();
        self.setLayout(form_layout);
    
    def botao_atualizar_click(self):
        html = self.fs.ler_raw( self.path_regra );
        self.tb.setHtml(html);