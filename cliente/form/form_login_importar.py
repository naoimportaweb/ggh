import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QFormLayout, QLabel, QMessageBox;
from PySide6 import QtWidgets;

from classes.conexao.xmpp_client import XMPPCliente;
from api.fsseguro import FsSeguro;
from classes.grupo import Grupo;

class FormImportar(QDialog):
    def __init__(self, parent=None):
        super(FormImportar, self).__init__(parent)
        #self.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.15);")
        self.setWindowTitle("Grupo")
        self.setGeometry(400, 400, 800, 500)
        #self.form_main = parent;
        #btn_gerar_imagem = QPushButton("Responder")
        #btn_gerar_imagem.clicked.connect(self.btn_gerar_imagem_click); 
        #self.form_main.addWidget( btn_gerar_imagem );
        #self.setLayout(self.form_main);
        chave="1234567890123456";
        grupo = Grupo("database.xmpp@xmpp.jp");
        print( grupo.importar_cliente( "/home/well/Desktop/chave.txt" , chave) );
        