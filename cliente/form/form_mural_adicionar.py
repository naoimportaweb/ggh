import sys, os, json;

sys.path.append("../"); # estamos em /form, 

#from PySide6.QtGui import *
from PySide6.QtWidgets import  QGridLayout, QTextEdit, QTabWidget,  QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from classes.mural import Mural;

class FormMuralAdicionar(QDialog):
    def __init__(self, xmpp_var, parent=None):
        super(FormMuralAdicionar, self).__init__(parent)
        self.setWindowTitle("Adicionar no Mural")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.xmpp_var = xmpp_var;
        self.main_layout = QVBoxLayout( self );        
        self.setLayout(self.main_layout);

        self.lb_titulo = QLabel("Título", self);
        self.titulo = QLineEdit(self);
        self.lb_nivel = QLabel("Nível", self);
        self.cmb_nivel = QComboBox();
        self.btn_salvar = QPushButton("Enviar mensagem");
        self.btn_salvar.clicked.connect( self.btn_salvar_click);

        widget1 = QWidget(self);
        widget1_layout = QHBoxLayout();
        widget1.setLayout(widget1_layout);
        widget1_layout.addWidget(self.lb_titulo);
        widget1_layout.addWidget(self.titulo);

        widget2 = QWidget(self);
        widget2_layout = QHBoxLayout();
        widget2.setLayout(widget2_layout);
        widget2_layout.addWidget(self.lb_nivel);
        widget2_layout.addWidget(self.cmb_nivel);

        widget3 = QWidget(self);
        widget3_layout = QHBoxLayout();
        widget3.setLayout(widget3_layout);
        widget3_layout.addStretch();
        widget3_layout.addWidget(self.btn_salvar);

        self.txt_mensagem = QTextEdit(self);

        self.main_layout.addWidget(widget1);
        self.main_layout.addWidget(widget2);
        self.main_layout.addWidget( self.txt_mensagem );
        self.main_layout.addWidget(widget3);

        self.cmb_nivel.clear();
        if len(self.xmpp_var.grupo.niveis) > 0:
            for nivel in self.xmpp_var.grupo.niveis:
                self.cmb_nivel.addItem(nivel.nome);
            self.cmb_nivel.setCurrentIndex(0);

    def btn_salvar_click(self, decisao):
        mural = Mural();
        mural.titulo = self.titulo.text();
        mural.mensagem =  self.txt_mensagem.toPlainText();
        mural.id_nivel =  self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id ;
        self.xmpp_var.adicionar_mensagem( "comandos.mural" ,"MuralComando", "criar", mural.toJson() );
        self.close();
