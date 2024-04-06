import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtWidgets import QSpacerItem,  QDateTimeEdit, QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt, QDateTime, QTime, QDate;

from classes.operacao import Operacao;

def widget_linha(form, layout, controls):
    widget1 = QWidget(form);
    widget1_layout = QHBoxLayout();
    widget1.setLayout(widget1_layout);
    for control in controls:
        print(type( control ).__name__);
        widget1_layout.addWidget( control );
    layout.addWidget(widget1);

def widget_tab(tab, titulo):
    page = QWidget(tab);
    page_layout=QVBoxLayout()
    page.setLayout(page_layout);
    tab.addTab( page, titulo );
    return page_layout;

def widget_tabela(form, colunas, tamanhos=None, double_click=None):
    table = QTableWidget(form)
    if double_click != None:
        table.doubleClicked.connect( double_click );
    js = {};
    for coluna in colunas:
        js[coluna] = "";
    table.setSelectionBehavior(QAbstractItemView.SelectRows); 
    table.setColumnCount(len(colunas));
    table.setEditTriggers(QAbstractItemView.NoEditTriggers);
    table.setHorizontalHeaderLabels(js.keys());
    if tamanhos != None:
        header = table.horizontalHeader() 
        for i in range(len(tamanhos)):
            header.setSectionResizeMode(i, tamanhos[i]);
    table.setRowCount(0)
    return table;

class FormOperacaoAdicionar(QDialog):
    def __init__(self, xmpp_var, operacao, parent=None):
        super(FormOperacaoAdicionar, self).__init__(parent)
        self.setWindowTitle("Operação")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.xmpp_var = xmpp_var;
        self.main_layout = QVBoxLayout( self );        
        self.operacao = operacao;

        self.txt_missao = None;
        self.txt_foco = None;
        self.tabela_atividade = None;
        self.tabela_niveis = None;
        self.txt_nome = None;
        self.data_inicio = None;
        self.data_fim = None;

        tab = QTabWidget();  
        self.main_layout.addWidget(tab);   
        
        self.layout_operacao( widget_tab( tab, "Operação" ) );
        self.layout_missao(   widget_tab( tab, "Missão" )) ;
        self.layout_foco  (   widget_tab( tab, "Foco" )) ;
        self.layout_atividades(widget_tab( tab, "Atividades" )) ;
        self.layout_niveis(   widget_tab( tab, "Niveis" )) ;
        
        btn_salvar =    QPushButton("Agora", self);
        btn_salvar.clicked.connect(self.btn_salvar_click);
        self.main_layout.addWidget( btn_salvar );
        self.setLayout(self.main_layout);

        #if operacao.id != None:
        self.txt_sigla.setText(operacao.sigla);
        self.txt_nome.setText(operacao.nome);
        self.txt_foco.setPlainText(operacao.foco);
        self.txt_missao.setPlainText(operacao.missao);
        self.data_fim.setDateTime(    QDateTime.fromString( operacao.data_fim, "yyyy-MM-dd HH:mm:ss"));
        self.data_inicio.setDateTime( QDateTime.fromString( operacao.data_inicio, "yyyy-MM-dd HH:mm:ss"));


    def layout_missao(self, layout):
        self.txt_missao = QTextEdit(self);
        widget_linha(self, layout, [ QLabel("Missão")  ]);
        widget_linha(self, layout, [ self.txt_missao ]);

    def layout_foco(self, layout):
        self.txt_foco = QTextEdit(self);
        widget_linha(self, layout, [ QLabel("Foco")  ]);
        widget_linha(self, layout, [ self.txt_foco ]);

    def layout_atividades(self, layout):
        self.tabela_atividade = widget_tabela(self, ["Título"], tamanhos=[QHeaderView.Stretch], double_click=self.tabela_atividade_click);
        layout.addWidget(self.tabela_atividade);

    def layout_niveis(self, layout):
        self.tabela_niveis = widget_tabela(self, ["Nome"], tamanhos=[QHeaderView.Stretch], double_click=self.tabela_nivel_click);
        layout.addWidget( self.tabela_niveis );
    
    def layout_operacao(self, layout):
        self.txt_sigla =   QLineEdit(self);
        self.txt_nome =    QLineEdit(self);
        self.data_inicio = QDateTimeEdit(self);
        self.data_fim =    QDateTimeEdit(self);
        btn_data_inicio_agora = QPushButton("Agora", self);
        btn_data_fim_agora =    QPushButton("Agora", self);

        self.data_inicio.setDisplayFormat("yyyy-MM-dd HH:mm:ss");
        self.data_fim.setDisplayFormat("yyyy-MM-dd HH:mm:ss");
        btn_data_inicio_agora.clicked.connect(self.btn_data_inicio_agora_click); 
        btn_data_fim_agora.clicked.connect(self.btn_data_fim_agora_click); 

        widget_linha(self, layout, [ QLabel("Sigla") , self.txt_sigla ]);
        widget_linha(self, layout, [ QLabel("Operação") , self.txt_nome ]);
        widget_linha(self, layout, [ QLabel("Início"), self.data_inicio, btn_data_inicio_agora, QLabel("Fim"), self.data_fim, btn_data_fim_agora]);
        layout.addStretch();
    def tabela_nivel_click(self):
        return;
    def tabela_atividade_click(self):
        return;
    def btn_data_inicio_agora_click(self):
        self.data_inicio.setMinimumDate(QDate.currentDate())
    def btn_data_fim_agora_click(self):
        self.data_fim.setMinimumDate(QDate.currentDate())
    def btn_salvar_click(self):
        return;
