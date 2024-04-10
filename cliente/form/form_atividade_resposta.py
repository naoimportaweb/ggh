import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;
from PySide6.QtWidgets import QLabel, QTextEdit, QTabWidget, QDialog, QHBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton;

from classes.atividade_resposta import AtividadeResposta;
from form.funcoes import Utilitario;

class FormAtividadeResposta(QDialog):
    def __init__(self, xmpp_var, atividade, index_resposta=None, parent=None):
        super(FormAtividadeResposta, self).__init__(parent)
        self.setWindowTitle("Responder Atividade")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.xmpp_var = xmpp_var;
        self.atividade = atividade;
        #if index_resposta == None:
        #    self.index_resposta = self.atividade.adicionar_resposta( self.xmpp_var.cliente.id, 0, "");
        #else:
        self.index_resposta = index_resposta;
        #self.txt_codigo = None;
        self.txt_resposta = None;
        self.txt_atividade = None;
        self.main_layout = QVBoxLayout( self );
        tab = QTabWidget();  
        self.main_layout.addWidget(tab);   
        
        page_atividade_reposta_layout = Utilitario.widget_tab(tab, "Resposta");
        self.layout_principal( page_atividade_reposta_layout );
        page_atividade_layout = Utilitario.widget_tab(tab, "Atividade");
        self.layout_atividade( page_atividade_layout );
        page_recomendacao_layout = Utilitario.widget_tab(tab, "Recomendações");
        self.layout_recomendacao( page_recomendacao_layout );
        page_aprovacao_layout = Utilitario.widget_tab(tab, "Aprovação");
        self.layout_aprovacao( page_aprovacao_layout );

        self.setLayout(self.main_layout);

    def layout_principal(self, layout):
        #self.txt_codigo = QTextEdit(self);
        #self.txt_codigo.setReadOnly(True);
        self.txt_resposta = QTextEdit(self);
        #Utilitario.widget_linha(self, layout, [QLabel("Códio único"), self.txt_codigo]);
        if self.index_resposta != None:
            self.txt_resposta.setPlainText( self.atividade.respostas[self.index_resposta].resposta );
            #self.txt_codigo.setText( self.atividade.respostas[self.index_resposta].chave_publica );
        layout.addWidget( self.txt_resposta );
        if self.index_resposta == None or ( self.atividade.respostas[self.index_resposta].data_avaliador == None and self.xmpp_var.cliente.id == self.atividade.respostas[self.index_resposta].id_cliente):
            btn_salvar = QPushButton("Responder");
            btn_salvar.clicked.connect(self.btn_click_salvar); 
            Utilitario.widget_linha(self, layout, [btn_salvar], stretch_inicio=True);
        
    def layout_atividade(self, layout):
        self.txt_atividade = QTextEdit(self);
        self.txt_atividade.setPlainText(  self.atividade.atividade   );
        layout.addWidget( self.txt_atividade );

    def layout_recomendacao(self, layout):
        self.txt_recomendacao = QTextEdit(self);
        path_html = self.xmpp_var.grupo.path_grupo_html + "/recomendacao.html";
        self.txt_recomendacao.setHtml(self.xmpp_var.cliente.fs.ler_raw( path_html ));
        layout.addWidget( self.txt_recomendacao );

    def layout_aprovacao(self, layout):
        self.txt_comentario = QTextEdit(self);
        layout.addWidget( self.txt_comentario );
        
        if self.index_resposta != None:
            if self.xmpp_var.cliente.posso_tag("atividade_corrigir") and self.atividade.respostas[self.index_resposta].id_status == 0:
                self.txt_comentario.setPlainText(self.atividade.respostas[self.index_resposta].consideracao_avaliador);
                btn_aprovar = QPushButton("APROVAR")
                btn_reprovar = QPushButton("REPROVAR")
                btn_reprovar.setStyleSheet("background-color: red; color: black");
                btn_aprovar.setStyleSheet("background-color: green; color: black");
                btn_aprovar.clicked.connect(self.btn_click_aprovar);
                btn_reprovar.clicked.connect(self.btn_click_reprovar);
                self.cb_pontos = QComboBox(self);
                for i in range( self.atividade.pontos_maximo ):
                    self.cb_pontos.addItem('Ponto: ' + str(i + 1));
                Utilitario.widget_linha(self, layout, [btn_reprovar, btn_aprovar], stretch_inicio=True);
            if self.atividade.respostas[self.index_resposta].id_status == 1:
                self.txt_comentario.setPlainText( "REPROVADO\n\n" + self.atividade.respostas[self.index_resposta].consideracao_avaliador);
            elif self.atividade.respostas[self.index_resposta].id_status == 2:
                self.txt_comentario.setPlainText( "APROVADO, ganhou " + str(self.atividade.respostas[self.index_resposta].pontos)  + " pontos\n\n" +  self.atividade.respostas[self.index_resposta].consideracao_avaliador);

    def funcao_enviar_aprovacao_reprovacao(self, decisao):
        self.atividade.respostas[self.index_resposta].consideracao_avaliador = self.txt_comentario.toPlainText();
        self.atividade.respostas[self.index_resposta].id_status = decisao;
        self.atividade.respostas[self.index_resposta].pontos = self.cb_pontos.currentIndex() + 1;
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "resposta_aprovar_reprovar", self.atividade.respostas[self.index_resposta].toJson());
        self.atividade.salvar(self.xmpp_var.cliente.chave_local, self.xmpp_var.cliente.path_atividade);
        self.close();
    def btn_click_reprovar(self):
        self.funcao_enviar_aprovacao_reprovacao(1);
    def btn_click_aprovar(self):
        self.funcao_enviar_aprovacao_reprovacao(2);
    def btn_click_salvar(self):
        if self.index_resposta == None:
            r = AtividadeResposta();
            r.id_atividade = self.atividade.id;
            r.resposta = self.txt_resposta.toPlainText();
            self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "resposta_adicionar", r.toJson());
            self.atividade.respostas.append(r);
            self.form_main.atualizar_respostas();
            self.atividade.salvar(self.xmpp_var.cliente.chave_local, self.xmpp_var.cliente.path_atividade);
            self.close();
        else:
            self.atividade.respostas[self.index_resposta].resposta = self.txt_resposta.toPlainText();
            self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "resposta_salvar", self.atividade.respostas[self.index_resposta].toJson());
            self.form_main.atualizar_respostas();
            self.atividade.salvar(self.xmpp_var.cliente.chave_local, self.xmpp_var.cliente.path_atividade);
            self.close();