import sys, os, json, base64, re, requests;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import *
from PySide6 import QtWidgets;
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from form.form_atividade_resposta import FormAtividadeResposta

class FormEditarAtividade(QDialog):
    def __init__(self, cliente, xmpp_var, atividade, parent=None):
        super(FormEditarAtividade, self).__init__(parent);
        self.cliente = cliente;
        self.xmpp_var = xmpp_var;
        self.atividade = atividade;
        self.setWindowTitle("Atividade");
        self.setGeometry(400, 400, 800, 500);
        self.main_layout = QVBoxLayout( self );
        self.textEditAtividade = None;
        self.table = None;

        tab =       QTabWidget();        
        self.main_layout.addWidget(tab);

        if atividade.id_cliente == self.cliente.id and self.xmpp_var.cliente.posso_tag("atividade_criar"):
            self.widget_botton = QWidget();
            self.botton_layout = QHBoxLayout();
            self.widget_botton.setLayout( self.botton_layout );
            self.btn_salvar = QPushButton("Salvar")
            self.btn_salvar.clicked.connect(self.btn_click_salvar); 
            self.botton_layout.addStretch();
            self.botton_layout.addWidget( self.btn_salvar );
            self.main_layout.addWidget(self.widget_botton);

        page_atividade = QWidget(tab);
        page_atividade_layout = QVBoxLayout();
        page_atividade.setLayout(page_atividade_layout);
        tab.addTab(page_atividade,'Atividade');

        page_correcao = QWidget(tab);
        page_correcao_layout = QVBoxLayout();
        page_correcao.setLayout(page_correcao_layout);
        tab.addTab(page_correcao,'Correção');

        page_respostas = QWidget(tab);
        page_respostas_layout = QGridLayout();
        page_respostas.setLayout(page_respostas_layout);
        tab.addTab(page_respostas,'Respostas');

        if atividade.id_cliente == self.cliente.id and self.xmpp_var.cliente.posso_tag("atividade_criar"):
            page_recomendacao_questao = QWidget(tab);
            page_recomendacao_questao_layout = QVBoxLayout();
            page_recomendacao_questao.setLayout(page_recomendacao_questao_layout);
            tab.addTab(page_recomendacao_questao,'Recomendação Correção');

        self.layout_resposta(  page_respostas_layout ,           self.atividade);
        self.layout_atividade( page_atividade_layout,            self.atividade);
        self.layout_correcao(  page_correcao_layout,             self.atividade);
        self.page_recomendacao_questao_layout(  page_recomendacao_questao_layout, self.atividade);
        self.showMaximized() 
    
    def layout_correcao(self, layout, atividade):
        layout.addWidget( QLabel("Pontuação máxima em caso de acerto:", self) );
        self.txt_pontos_maximo = QLineEdit(self);
        layout.addWidget( self.txt_pontos_maximo );

        layout.addWidget( QLabel("Pontuação do corretor:", self) );
        self.txt_pontos_corretor_maximo = QLineEdit(self);
        layout.addWidget( self.txt_pontos_corretor_maximo );
        self.txt_pontos_corretor_maximo.setText(str( self.atividade.pontos_correcao_maximo ));
        self.txt_pontos_maximo.setText( str(self.atividade.pontos_maximo) );
        layout.addStretch();

    def page_recomendacao_questao_layout(self, layout, atividade):
        self.txt_recomendacao = QTextEdit(self);
        self.txt_recomendacao.setPlainText( atividade.instrucao_correcao );
        layout.addWidget( self.txt_recomendacao );

    def layout_atividade(self, layout, atividade):
        label = QLabel("Atividade", self);
        self.titulo = QLineEdit(self);

        page = QWidget(self);
        page_layout = QHBoxLayout();
        page.setLayout(page_layout);
        page_layout.addWidget(label);
        page_layout.addWidget(self.titulo);

        btn_aprovar = QPushButton("Aprovar")
        btn_aprovar.clicked.connect( self.btn_click_aprovar);
        btn_reprovar = QPushButton("Reprovar")
        btn_reprovar.clicked.connect( self.btn_click_reprovar);
        btn_editar = QPushButton("Editar")
        btn_editar.clicked.connect( self.btn_click_editar);
        btn_reprovar.setStyleSheet("background-color: red;    color: black");
        btn_aprovar.setStyleSheet( "background-color: green;  color: black");
        btn_editar.setStyleSheet(  "background-color: yellow; color: black");
        if self.atividade.id_status == 0:
            page_layout.addWidget(btn_aprovar);
            page_layout.addWidget(btn_reprovar);
        elif self.atividade.id_status == 1:
            page_layout.addWidget(btn_aprovar);
            page_layout.addWidget(btn_editar);
        elif self.atividade.id_status == 2:
            page_layout.addWidget(btn_reprovar);
            page_layout.addWidget(btn_editar);

        layout.addWidget( page );

        self.textEditAtividade = QTextEdit(self);
        self.textEditAtividade.setPlainText( atividade.atividade );
        self.titulo.setText( self.atividade.titulo );
        layout.addWidget( self.textEditAtividade );
    
    def btn_click_aprovar(self):
        self.atividade.id_status = 2;
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "atividade_aprovar_reprovar", self.atividade.toJson() );
    
    def btn_click_reprovar(self):
        self.atividade.id_status = 1;
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "atividade_aprovar_reprovar", self.atividade.toJson() );
    
    def btn_click_editar(self):
        self.atividade.id_status = 0;
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "atividade_aprovar_reprovar", self.atividade.toJson() );
    
    def atualizar_respostas(self):
        colunas = [{"Título" : "", "Status": "", "Pontos" : "", "Data" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents()
        self.table.setColumnCount(4)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        header = self.table.horizontalHeader() ;# https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setRowCount( len(  self.atividade.respostas  ) );
        index = 0;
        for resposta in self.atividade.respostas:
            self.table.setItem( index, 0, QTableWidgetItem( resposta.resposta       ) );
            self.table.setItem( index, 1, QTableWidgetItem( resposta.getStatus()    ) );
            self.table.setItem( index, 2, QTableWidgetItem( resposta.getPontos()    ) );
            self.table.setItem( index, 3, QTableWidgetItem( resposta.data           ) );
            index = index + 1;
    
    def table_resposta_double(self):
        f = FormAtividadeResposta(self.xmpp_var, self.atividade, index_resposta=self.table.currentRow(), parent=self );
        f.exec();

    def layout_resposta(self, layout, atividade):
        layout.addWidget( QLabel("Repostas", self) );
        self.table = QTableWidget(self)
        self.table.doubleClicked.connect(self.table_resposta_double)
        layout.addWidget(self.table);
        self.atualizar_respostas();
        if self.atividade.id_status == 2:
            widget_botton_resposta = QWidget();
            botton_layout_resposta = QHBoxLayout();
            widget_botton_resposta.setLayout(    botton_layout_resposta );
            btn_salvar_resposta = QPushButton("Enviar uma nova resposta")
            btn_salvar_resposta.clicked.connect( self.btn_click_adicionar_resposta); 
            botton_layout_resposta.addStretch();
            botton_layout_resposta.addWidget(    btn_salvar_resposta );
            layout.addWidget( widget_botton_resposta );
    
    def btn_click_adicionar_resposta(self):
        f = FormAtividadeResposta(self.xmpp_var, self.atividade, index_resposta=None, parent=self );
        f.exec();

    def btn_click_adicionar_resposta_callback(self, message):
        print("tem que dizer que tem que atualizar listagem.");
    
    def btn_click_salvar(self):
        self.atividade.atividade =                 self.textEditAtividade.toPlainText();
        self.atividade.titulo =                    self.titulo.text();
        self.atividade.instrucao_correcao =        self.txt_recomendacao.toPlainText();
        self.atividade.pontos_maximo =             int(self.txt_pontos_maximo.text());
        self.atividade.pontos_correcao_maximo    = int(self.txt_pontos_corretor_maximo.text());
        self.atividade.instrucao_correcao = self.txt_recomendacao.toPlainText();
        self.xmpp_var.adicionar_mensagem( "comandos.atividade" ,"AtividadeComando", "salvar", self.atividade.toJson() );
#