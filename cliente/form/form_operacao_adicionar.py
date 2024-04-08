import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtWidgets import QSpacerItem,  QDateTimeEdit, QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt, QDateTime, QTime, QDate;

from classes.operacao import Operacao;
from form.funcoes import Utilitario;

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
        self.txt_nome = None;
        self.data_inicio = None;
        self.data_fim = None;

        tab = QTabWidget();  
        self.main_layout.addWidget(tab);   
        
        self.layout_operacao(  Utilitario.widget_tab( tab,  "Operação"  )) ;
        self.layout_missao(    Utilitario.widget_tab( tab,  "Missão"    )) ;
        self.layout_foco  (    Utilitario.widget_tab( tab,  "Foco"      )) ;
        self.layout_atividades(Utilitario.widget_tab( tab, "Atividades")) ;
        
        btn_salvar =    QPushButton("Salvar Operação", self);
        btn_salvar.clicked.connect(self.btn_salvar_click);
        self.main_layout.addWidget( btn_salvar );
        self.setLayout(self.main_layout);

        #if operacao.id != None:
        self.txt_sigla.setText(operacao.sigla);
        self.txt_nome.setText(operacao.nome);
        self.txt_foco.setPlainText(operacao.foco);
        self.txt_missao.setPlainText(operacao.missao);
        self.data_fim.setDateTime(    QDateTime.fromString( operacao.data_fim,    "yyyy-MM-dd HH:mm:ss"));
        self.data_inicio.setDateTime( QDateTime.fromString( operacao.data_inicio, "yyyy-MM-dd HH:mm:ss"));

    def atualizar_tabela_atividades(self):
        self.tabela_atividade.setRowCount( len( self.operacao.atividades ) );
        for i in range(len(self.operacao.atividades)):
            self.tabela_atividade.setItem( i, 0, QTableWidgetItem( self.operacao.atividades[1].titulo ) );

    def layout_missao(self, layout):
        self.txt_missao = QTextEdit(self);
        Utilitario.widget_linha(self, layout, [ QLabel("Missão")  ]);
        Utilitario.widget_linha(self, layout, [ self.txt_missao ]);

    def layout_foco(self, layout):
        self.txt_foco = QTextEdit(self);
        Utilitario.widget_linha(self, layout, [ QLabel("Foco")  ]);
        Utilitario.widget_linha(self, layout, [ self.txt_foco ]);

    def layout_atividades(self, layout):
        self.tabela_atividade = Utilitario.widget_tabela(self, ["Título"], tamanhos=[QHeaderView.Stretch], double_click=self.tabela_atividade_click);
        layout.addWidget(self.tabela_atividade);
    
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

        Utilitario.widget_linha(self, layout, [ QLabel("Sigla") , self.txt_sigla ]);
        Utilitario.widget_linha(self, layout, [ QLabel("Operação") , self.txt_nome ]);
        Utilitario.widget_linha(self, layout, [ QLabel("Início"), self.data_inicio, btn_data_inicio_agora, QLabel("Fim"), self.data_fim, btn_data_fim_agora]);
        layout.addStretch();
    def tabela_atividade_click(self):
        return;
    def btn_data_inicio_agora_click(self):
        self.data_inicio.setMinimumDate(QDate.currentDate())
    def btn_data_fim_agora_click(self):
        self.data_fim.setMinimumDate(QDate.currentDate())
    def btn_salvar_click(self):
        self.operacao.sigla = self.txt_sigla.text();
        self.operacao.nome = self.txt_nome.text();
        self.operacao.missao = self.txt_missao.toPlainText();
        self.operacao.foco = self.txt_foco.toPlainText();
        self.operacao.data_inicio = self.data_inicio.dateTime().toString("yyyy-MM-dd HH:mm:ss");
        self.operacao.data_fim = self.data_fim.dateTime().toString("yyyy-MM-dd HH:mm:ss");
        self.xmpp_var.adicionar_mensagem( "comandos.operacao" ,"OperacaoComando", "salvar", self.operacao.toJson() );
        return;
#{"nome" : "operacao", "fields" : ["id", "sigla", "nome", "id_grupo", "id_operacao_status", "data_inicio", "data_fim", "missao", "foco"]},