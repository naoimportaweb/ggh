import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import *

class FormAtividadeResposta(QDialog):
    def __init__(self, atividade, index_resposta=None, parent=None):
        super(FormAtividadeResposta, self).__init__(parent)
        self.setWindowTitle("Grupo")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.atividade = atividade;
        layout = QVBoxLayout(self);
        self.textEditAtividade = QTextEdit(self);
        if index_resposta != None:
            self.textEditAtividade.setPlainText( atividade.respostas[index_resposta].resposta );
        layout.addWidget( self.textEditAtividade );
        
        if index_resposta == None or atividade.respostas[index_resposta].data_avaliador == None:
            widget_botton = QWidget();
            botton_layout = QHBoxLayout();
            widget_botton.setLayout( botton_layout );
            btn_salvar = QPushButton("Responder")
            btn_salvar.clicked.connect(self.btn_click_salvar); 
            botton_layout.addWidget( btn_salvar );
            layout.addWidget(widget_botton);
        self.setLayout(layout);
    def btn_click_salvar(self):
        print("...");