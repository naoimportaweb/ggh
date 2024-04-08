import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QPalette, QFont;
from PySide6.QtCore import Qt;
from PySide6.QtWidgets import QTextEdit, QTabWidget, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QPushButton;
#from PySide6.QtWidgets import QGridLayout, QTextEdit, QTabWidget,  QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;


from classes.atividade_resposta import AtividadeResposta;

class FormAtividadeCorrigir(QDialog):
    def __init__(self, xmpp_var, correcao, parent=None):
        super(FormAtividadeCorrigir, self).__init__(parent)
        self.setWindowTitle("Corrigir Atividade")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.xmpp_var = xmpp_var;
        self.correcao = correcao;
        self.txt_resposta = None;
        self.txt_atividade = None;
        self.main_layout = QVBoxLayout( self );
        tab = QTabWidget();  
        self.main_layout.addWidget(tab);   
        
        page_atividade_reposta = QWidget(tab);
        page_atividade_reposta_layout = QVBoxLayout();
        page_atividade_reposta.setLayout(page_atividade_reposta_layout);
        tab.addTab(page_atividade_reposta,'Reposta');
        self.layout_principal( page_atividade_reposta_layout );

        page_atividade = QWidget(tab);
        page_atividade_layout = QVBoxLayout();
        page_atividade.setLayout(page_atividade_layout);
        tab.addTab(page_atividade,'Atividade');
        self.layout_atividade( page_atividade_layout );

        page_recomendacao = QWidget(tab);
        page_recomendacao_layout = QVBoxLayout();
        page_recomendacao.setLayout(page_recomendacao_layout);
        tab.addTab(page_recomendacao,'Recomendações');
        self.layout_recomendacao( page_recomendacao_layout );

        page_aprovacao = QWidget(tab);
        page_aprovacao_layout = QVBoxLayout();
        page_aprovacao.setLayout(page_aprovacao_layout);
        tab.addTab(page_aprovacao,'Aprovação');
        self.layout_aprovacao( page_aprovacao_layout );

        self.setLayout(self.main_layout);

    def layout_principal(self, layout):
        self.txt_resposta = QTextEdit(self);
        self.txt_resposta.setPlainText( self.correcao["resposta"] );
        layout.addWidget( self.txt_resposta );
        
    def layout_atividade(self, layout):
        self.txt_atividade = QTextEdit(self);
        self.txt_atividade.setPlainText(  self.correcao["atividade"]   );
        layout.addWidget( self.txt_atividade );

    def layout_recomendacao(self, layout):
        self.txt_recomendacao = QTextEdit(self);
        self.txt_recomendacao.setHtml(self.correcao["instrucao_correcao"]);
        layout.addWidget( self.txt_recomendacao );

    def layout_aprovacao(self, layout):
        self.txt_comentario = QTextEdit(self);
        layout.addWidget( self.txt_comentario );
        
        if self.xmpp_var.cliente.posso_tag("atividade_corrigir"):
            widget_botton = QWidget();
            botton_layout = QHBoxLayout();
            widget_botton.setLayout( botton_layout );
            btn_aprovar = QPushButton("APROVAR")
            btn_reprovar = QPushButton("REPROVAR")
            btn_reprovar.setStyleSheet("background-color: red; color: black");
            btn_aprovar.setStyleSheet("background-color: green; color: black");
            btn_aprovar.clicked.connect(self.btn_click_aprovar);
            btn_reprovar.clicked.connect(self.btn_click_reprovar);
            self.cb_pontos = QComboBox(self);
            for i in range( self.correcao["pontos_maximo"] ):
                self.cb_pontos.addItem('Ponto: ' + str(i + 1));
            botton_layout.addWidget( btn_reprovar );
            botton_layout.addStretch();
            botton_layout.addWidget(self.cb_pontos);
            botton_layout.addWidget( btn_aprovar );
            layout.addWidget(widget_botton);

    def funcao_enviar_aprovacao_reprovacao(self, decisao):
        self.correcao["consideracao_avaliador"] = self.txt_comentario.toPlainText();
        self.correcao["id_status"] = decisao;
        self.correcao["pontos"] = self.cb_pontos.currentIndex() + 1;
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "resposta_aprovar_reprovar", self.correcao );
        self.close();
    def btn_click_reprovar(self):
        self.funcao_enviar_aprovacao_reprovacao(1);
    def btn_click_aprovar(self):
        self.funcao_enviar_aprovacao_reprovacao(2);
