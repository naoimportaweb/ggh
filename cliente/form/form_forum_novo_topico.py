import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QPalette, QFont;
from PySide6.QtCore import Qt;
from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QTabWidget, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QPushButton;
from form.ui.combobox import ComboBox;
from form.funcoes import Utilitario;

CACHE_CMB_NIVEL = 'form_forum_novo_topico.cmb_nivel';

class FormForumNovoTopico(QDialog):
    def __init__(self, xmpp_var, callback, parent=None):
        super(FormForumNovoTopico, self).__init__(parent)
        self.setWindowTitle("Tópico do Forum")
        self.setGeometry(400, 400, 800, 500)
        self.callback = callback;
        self.main_layout = QVBoxLayout( self );
        self.cmb_nivel = ComboBox(self, CACHE_CMB_NIVEL, configuracao=xmpp_var.cliente.configuracao);
        self.main_layout .addWidget( self.cmb_nivel );
        self.cmb_nivel.addArrayObject(xmpp_var.grupo.niveis, "id", "nome");
        self.label = QLabel("Título");
        self.txt_texto = QLineEdit(self);
        Utilitario.widget_linha(self, self.main_layout, [ self.label, self.txt_texto ]);
        Utilitario.widget_linha(self, self.main_layout, [ QLabel("Descrição:") ]);
        self.descricao = QTextEdit(self);
        self.main_layout.addWidget( self.descricao );
        self.btn = QPushButton("Salvar");
        self.btn.clicked.connect(self.btn_click);
        self.main_layout.addWidget( self.btn );
        self.setLayout(self.main_layout);

    def btn_click(self):
        self.callback(self.cmb_nivel.getSelected().key, self.txt_texto.text(), self.descricao.toPlainText(), self );
