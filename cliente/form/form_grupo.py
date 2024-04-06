import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtWidgets import QApplication, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from form.painel_chat import PainelChat
from form.painel_regras import PainelRegras
from form.painel_recomendacoes import PainelRecomendacoes
from form.painel_conhecimento import PainelConhecimento
from form.painel_atividade import PainelAtividade
from form.painel_corrigir import PainelCorrigir;
from form.painel_mural import PainelMural;
from form.painel_conta import PainelConta;
from form.painel_operacao import PainelOperacao;

class FormGrupo(QtWidgets.QWidget):
    def __init__(self, form_pai, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs);
        self.xmpp_var = None;
        self.layout1 = QVBoxLayout()
        self.form_pai = form_pai;

        self.b11 = QPushButton("Conta")
        self.b11.clicked.connect( self.botao_conta_click )
        self.layout1.addWidget(self.b11)
        
        self.b4 = QPushButton("Chat")
        self.b4.clicked.connect( self.botao_chat_click )
        self.layout1.addWidget(self.b4)

        self.b10 = QPushButton("Mural")
        self.b10.clicked.connect( self.botao_mural_click )
        self.layout1.addWidget(self.b10)

        self.b5 = QPushButton("Regras")
        self.b5.clicked.connect( self.botao_regras_click )
        self.layout1.addWidget(self.b5)

        self.b6 = QPushButton("Recomendações")
        self.b6.clicked.connect( self.botao_recomendacoes_click )
        self.layout1.addWidget(self.b6)

        self.b7 = QPushButton("Conhecimento")
        self.b7.clicked.connect( self.botao_conhecimento_click )
        self.layout1.addWidget(self.b7)

        self.b8 = QPushButton("Atividades")
        self.b8.clicked.connect( self.botao_atividade_click )
        self.layout1.addWidget(self.b8)
        
        self.layout = QHBoxLayout();
        self.layout.addLayout( self.layout1 );
        self.setLayout( self.layout );
    
    def ativar_layout_especifico(self, widget_type_name):
        if self.widget_atual.__class__.__name__ == widget_type_name:
            return;
        for buffer in self.widgets:
            if buffer.__class__.__name__ == widget_type_name:
                self.layout.addWidget( buffer );
                buffer.atualizar_tela();
                buffer.ativo = True;
                self.widget_atual = buffer;
            else:
                buffer.setParent( None );
                buffer.ativo = False;
    
    def botao_operacoes_click(self):
        self.ativar_layout_especifico( "PainelOperacao" );
    def botao_conta_click(self):
        self.ativar_layout_especifico( "PainelConta" );
    def botao_mural_click(self):
        self.ativar_layout_especifico( "PainelMural" );
    def botao_atividade_click(self):
        self.ativar_layout_especifico( "PainelAtividade" );
    def botao_conhecimento_click(self):
        self.ativar_layout_especifico( "PainelConhecimento" );
    def botao_chat_click(self):
        self.ativar_layout_especifico( "PainelChat" );
    def botao_regras_click(self):
        self.ativar_layout_especifico( "PainelRegras" );
    def botao_recomendacoes_click(self):
        self.ativar_layout_especifico( "PainelRecomendacoes" );
    def botao_correcoes_click(self):
        self.ativar_layout_especifico( "PainelCorrigir" );

    def set_grupo(self, xmpp_var):
        self.xmpp_var = xmpp_var;
        self.xmpp_var.set_callback(self.evento_mensagem);
        self.setWindowTitle( xmpp_var.cliente.jid +  " <=#=> " +  xmpp_var.grupo.jid );

        self.xmpp_var.adicionar_mensagem( "comandos.ambiente" ,"AmbienteComando", "dados", {});
        self.xmpp_var.adicionar_mensagem( "comandos.html" ,"HtmlComando", "get", {"path" : "regras.html"});
        self.xmpp_var.adicionar_mensagem( "comandos.html" ,"HtmlComando", "get", {"path" : "recomendacao.html"});

        if self.xmpp_var.cliente.posso_tag("atividade_corrigir"):
            self.b9 = QPushButton("Correções")
            self.b9.clicked.connect( self.botao_correcoes_click )
            self.layout1.addWidget(self.b9)
        #if self.xmpp_var.cliente.posso_tag("operacao_criar"):
        self.b12 = QPushButton("Operações")
        self.b12.clicked.connect( self.botao_operacoes_click )
        self.layout1.addWidget(self.b12)
        self.layout1.addStretch();
        self.carregar_panel();

    def carregar_panel( self ):
        self.widgets = [PainelConta(self.xmpp_var), PainelChat(self.xmpp_var), PainelRegras(self.xmpp_var), PainelRecomendacoes(self.xmpp_var), PainelConhecimento( self.xmpp_var ),
                       PainelAtividade( self.xmpp_var ), PainelCorrigir(self.xmpp_var), 
                       PainelMural(self.xmpp_var), PainelOperacao(self.xmpp_var) ];
        self.widgets[0].ativo = True;
        self.layout.addWidget( self.widgets[0] );
        self.widgets[0].atualizar_tela();
        self.widget_atual = self.widgets[0];

    def evento_mensagem(self, de, texto, message, conteudo_js):
        if conteudo_js["comando"] == "AmbienteComando" and conteudo_js["funcao"] == "dados":
            if conteudo_js["versao"] != self.xmpp_var.dados["versao"]:
                print("\033[41mAtenção, a versão do servidor é incompatível com a versão do cliente. A versão do servidor é: " + conteudo_js["versao"] + " \033[0m");
                self.close();
        for buffer in self.widgets:
            buffer.evento_mensagem(de, texto, message, conteudo_js);
    
    def closeEvent(self, event):
        event.accept();
        self.xmpp_var.disconnect();

    def callback_cliente_cadastro(self):
        return;
