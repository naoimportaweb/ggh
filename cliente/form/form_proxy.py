
import sys, os, json, traceback;

sys.path.append("../"); # estamos em /form, 

#from PySide6.QtGui import *
from PySide6.QtWidgets import QMessageBox, QFileDialog, QFormLayout, QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from classes.conexao.xmpp_client import XMPPCliente;
from api.fsseguro import FsSeguro;
from classes.grupo import Grupo;
from form.funcoes import Utilitario;

class FormProxy(QDialog):
    def __init__(self, parent=None):
        super(FormProxy, self).__init__(parent)
        self.setWindowTitle("Proxy")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.main_layout = QVBoxLayout( );
        
        self.protocolo_proxy = QLineEdit('http', self);
        self.servidor_proxy = QLineEdit('127.0.0.1', self);
        self.porta_proxy = QLineEdit('9051', self);

        layout = QFormLayout();
        layout.addRow(QLabel("Protocolo proxy"), self.protocolo_proxy);
        layout.addRow(QLabel("IP do proxy"),     self.servidor_proxy);
        layout.addRow(QLabel("Porta do Proxy"),  self.porta_proxy);
        widget2 = QWidget();
        widget2.setLayout( layout );
        self.main_layout.addWidget( widget2 );
        self.setLayout(self.main_layout);
        
        btn = QPushButton("Alterar proxy");
        btn.clicked.connect(self.btn_click); 
        Utilitario.widget_linha(self, self.main_layout, [btn], stretch_inicio=True);
    def btn_click(self):
        proxy = self.protocolo_proxy.text() + "://"+ self.servidor_proxy.text() +":" + self.porta_proxy.text();
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        self.close();

        