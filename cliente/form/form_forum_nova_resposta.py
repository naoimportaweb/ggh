import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QPalette, QFont;
from PySide6.QtCore import Qt;
from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QTabWidget, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QPushButton;
from form.ui.combobox import ComboBox;
from form.funcoes import Utilitario;


class FormForumNovaResposta(QDialog):
    def __init__(self, xmpp_var, callback, parent=None):
        super(FormForumNovaResposta, self).__init__(parent)
        self.setWindowTitle("Thread")
        self.setGeometry(400, 400, 800, 500)
        self.callback = callback;
        self.main_layout = QVBoxLayout( self );
        Utilitario.widget_linha(self, self.main_layout, [ QLabel("Texto:") ]);
        self.descricao = QTextEdit(self);
        self.descricao.setAcceptRichText(False);
        self.main_layout.addWidget( self.descricao );
        self.btn = QPushButton("Salvar");
        self.btn.clicked.connect(self.btn_click);
        self.main_layout.addWidget( self.btn );
        self.setLayout(self.main_layout);

    def btn_click(self):
        self.callback( self.descricao.toPlainText(), self );
