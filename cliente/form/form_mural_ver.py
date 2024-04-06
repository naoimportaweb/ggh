import sys, os, json;

sys.path.append("../"); # estamos em /form, 

#from PySide6.QtGui import *
from PySide6.QtWidgets import    QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from classes.mural import Mural;

class FormMuralVer(QDialog):
    def __init__(self, xmpp_var, mural, parent=None):
        super(FormMuralVer, self).__init__(parent)
        self.setWindowTitle("Grupo")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.xmpp_var = xmpp_var;
        self.main_layout = QVBoxLayout( self );        
        self.setLayout(self.main_layout);

        self.lb_titulo = QLabel("Título", self);
        self.titulo = QLineEdit(self);
        self.titulo.setReadOnly(True);

        widget1 = QWidget(self);
        widget1_layout = QHBoxLayout();
        widget1.setLayout(widget1_layout);
        widget1_layout.addWidget(self.lb_titulo);
        widget1_layout.addWidget(self.titulo);

        self.txt_mensagem = QTextEdit(self);
        self.txt_mensagem.setReadOnly(True);

        self.main_layout.addWidget(widget1);
        self.main_layout.addWidget( self.txt_mensagem );
        self.txt_mensagem.setPlainText( mural.mensagem );
        self.titulo.setText( mural.titulo );

