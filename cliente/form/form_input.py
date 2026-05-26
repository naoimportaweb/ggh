import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QPalette, QFont;
from PySide6.QtCore import Qt;
from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QTabWidget, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QPushButton;

from form.funcoes import Utilitario;

class FormInput(QDialog):
    def __init__(self, mensagem, callback, parent=None):
        super(FormInput, self).__init__(parent)
        self.setWindowTitle("Informe")
        self.setGeometry(400, 400, 800, 500)
        self.callback = callback;
        self.main_layout = QVBoxLayout( self );
        self.label = QLabel(mensagem);
        self.txt_texto = QLineEdit(self);
        Utilitario.widget_linha(self, self.main_layout, [ self.label, self.txt_texto ]);
        self.btn = QPushButton("Informar");
        self.btn.clicked.connect(self.btn_click);
        self.main_layout.addWidget( self.btn );
        self.setLayout(self.main_layout);
    def btn_click(self):
        self.callback( self.txt_texto.text() );
        self.close();