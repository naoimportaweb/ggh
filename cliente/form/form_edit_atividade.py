import sys, os, json, base64, re, requests;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import *
from PySide6 import QtWidgets;
from PySide6.QtWidgets import *
from PySide6.QtCore import *

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
        
        page_atividade = QWidget(tab);
        page_atividade_layout = QVBoxLayout();
        page_atividade.setLayout(page_atividade_layout);
        tab.addTab(page_atividade,'Atividade');

        page_respostas = QWidget(tab);
        page_respostas_layout = QGridLayout();
        page_respostas.setLayout(page_respostas_layout);
        tab.addTab(page_respostas,'Respostas');

        #page_tag = QWidget(tab);
        #page_tag_layout = QGridLayout();
        #page_tag.setLayout(page_tag_layout);
        #tab.addTab(page_tag,'TAGs');

        #page_apr = QWidget(tab);
        #page_apr_layout = QGridLayout();
        #page_apr.setLayout(page_apr_layout);
        #tab.addTab(page_apr,'Aprovação');
        
        #if self.xmpp_var.cliente.id == conhecimento.id_cliente and conhecimento.status == 0:
        #    self.b5 = QPushButton("Salvar Atividade")
        #    self.b5.clicked.connect( self.botao_salvar_conhecimento_click )
        #    page_inferior = QWidget(self);
        #    page_inferior_layout = QHBoxLayout();
        #    page_inferior.setLayout(page_inferior_layout);
        #    page_inferior_layout.addStretch();
        #   page_inferior_layout.addWidget(self.b5);
        #    self.main_layout.addWidget( page_inferior );
        #self.setLayout(self.main_layout);
        #self.layout_principal( page_elementos_layout, self.conhecimento);
        #self.layout_editor(    page_text_layout,      self.conhecimento);
        self.layout_resposta( page_respostas_layout ,       self.atividade);
        self.layout_atividade( page_atividade_layout,       self.atividade);
        self.showMaximized() 

    def layout_atividade(self, layout, atividade):
        self.textEditAtividade = QTextEdit(self);
        layout.addWidget( self.textEditAtividade );
    def layout_resposta(self, layout, atividade):
        layout.addWidget( QLabel("Repostas", self) );
        self.table = QTableWidget(self)
        colunas = [{"Título" : ""}];
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.table.resizeColumnsToContents()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(colunas[0].keys());
        self.table.setRowCount(0)
        layout.addWidget(self.table);
        self.table.setRowCount( len(  self.atividade.respostas  ) );
        index = 0;
        for resposta in self.atividade.respostas:
            self.table.setItem( index, 0, QTableWidgetItem( resposta.data ) );
            index = index + 1;
    #def layout_editor(self, layout, conhecimento):
    #    # TAB DE TEXTO -> CONHECIMENTO
    #    self.editor = TextEdit()
    #    self.editor.setAutoFormatting(QTextEdit.AutoAll)
    #    self.editor.selectionChanged.connect(self.update_format)
    #    font = QFont('Times', 12)
    #    self.editor.setFont(font)
    #    self.editor.setFontPointSize(12)
    #    self._format_actions = [ ]
    #    self.editor.setHtml( conhecimento.texto );
    #    layout.addWidget( QLabel("Conhecimento", self) );
    #    layout.addWidget(self.editor)
    #def layout_principal(self, layout, conhecimento):
    #    self.titulo = QLineEdit(conhecimento.titulo, self);
    #    self.cmb_nivel = QComboBox(); 
    #    self.cmb_nivel.clear();
    #    if len(self.xmpp_var.grupo.niveis) > 0:
    #        index = 0;
    #        for nivel in self.xmpp_var.grupo.niveis:
    #            self.cmb_nivel.addItem(nivel.nome);
    #            if nivel.id == conhecimento.id_nivel:
    #                self.cmb_nivel.setCurrentIndex(index)
    #            index += 1;
    #    layout.addWidget( QLabel("Nível do conhecimento", self) );
    #    layout.addWidget( self.cmb_nivel );
    #    layout.addWidget( QLabel("Título", self) );
    #    layout.addWidget( self.titulo);
    #    layout.addStretch();
    #def botao_salvar_conhecimento_click(self):
    #    self.conhecimento.setHtml( self.editor.toHtml() );
    #    self.conhecimento.titulo = self.titulo.text();
    #    self.conhecimento.id_nivel = self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id;
    #    self.xmpp_var.adicionar_mensagem("comandos.conhecimento" ,"ConhecimentoComando", "salvar", self.conhecimento.toJson() );
    #def block_signals(self, objects, b):
    #    for o in objects:
    #        o.blockSignals(b)
    #def update_format(self):
    #    self.block_signals(self._format_actions, True)
    #    self.block_signals(self._format_actions, False)
