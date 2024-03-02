import sys, os, json, base64, re, requests;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import *
#from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QTabWidget, QVBoxLayout, QGridLayout,  QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QFormLayout, QLabel, QMessageBox;
from PySide6 import QtWidgets;
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from form.text_edit import TextEdit;

#FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
#IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
#HTML_EXTENSIONS = ['.htm', '.html']

def hexuuid():
    return uuid.uuid4().hex

def splitext(p):
    return os.path.splitext(p)[1].lower()
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class FormEditarConhecimento(QDialog):
    def __init__(self, cliente, xmpp_var, conhecimento, parent=None):
        super(FormEditarConhecimento, self).__init__(parent);
        self.cliente = cliente;
        self.xmpp_var = xmpp_var;
        self.conhecimento = conhecimento;
        self.setWindowTitle("Conhecimento");
        self.setGeometry(400, 400, 800, 500);
        self.main_layout = QVBoxLayout( self );

        tab =       QTabWidget();        
        self.main_layout.addWidget(tab);
        
        page_elementos = QWidget(tab);
        page_elementos_layout = QVBoxLayout();
        page_elementos.setLayout(page_elementos_layout);
        tab.addTab(page_elementos,'Elementos textuais');

        page_text = QWidget(tab);
        page_text_layout = QGridLayout();
        page_text.setLayout(page_text_layout);
        tab.addTab(page_text,'Conhecimento');

        page_tag = QWidget(tab);
        page_tag_layout = QGridLayout();
        page_tag.setLayout(page_tag_layout);
        tab.addTab(page_tag,'TAGs');

        page_apr = QWidget(tab);
        page_apr_layout = QGridLayout();
        page_apr.setLayout(page_apr_layout);
        tab.addTab(page_apr,'Aprovação');
        
        if self.xmpp_var.cliente.id == conhecimento.id_cliente and conhecimento.status == 0:
            self.b5 = QPushButton("Salvar conhecimento")
            self.b5.clicked.connect( self.botao_salvar_conhecimento_click )
            page_inferior = QWidget(self);
            page_inferior_layout = QHBoxLayout();
            page_inferior.setLayout(page_inferior_layout);
            page_inferior_layout.addStretch();
            page_inferior_layout.addWidget(self.b5);
            self.main_layout.addWidget( page_inferior );

        self.setLayout(self.main_layout);
        self.layout_principal( page_elementos_layout, self.conhecimento);
        self.layout_editor(    page_text_layout,      self.conhecimento);
        self.layout_tag( page_tag_layout,             self.conhecimento);
        self.layout_aprovacao( page_apr_layout,       self.conhecimento);
        self.showMaximized() 

    def layout_tag(self, layout, conhecimento):
        layout.addWidget( QLabel("TAGs:", self) );

    def layout_aprovacao(self, layout, conhecimento):
        layout.addWidget( QLabel("Aprovação:", self) );

    def layout_editor(self, layout, conhecimento):
        # TAB DE TEXTO -> CONHECIMENTO
        self.editor = TextEdit()
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)
        font = QFont('Times', 12)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)
        self._format_actions = [ ]
        self.editor.setHtml( conhecimento.texto );
        layout.addWidget( QLabel("Conhecimento", self) );
        layout.addWidget(self.editor)

    def layout_principal(self, layout, conhecimento):
        self.titulo = QLineEdit(conhecimento.titulo, self);
        self.cmb_nivel = QComboBox(); 
        self.cmb_nivel.clear();
        if len(self.xmpp_var.grupo.niveis) > 0:
            index = 0;
            for nivel in self.xmpp_var.grupo.niveis:
                self.cmb_nivel.addItem(nivel.nome);
                if nivel.id == conhecimento.id_nivel:
                    self.cmb_nivel.setCurrentIndex(index)
                index += 1;
        layout.addWidget( QLabel("Nível do conhecimento", self) );
        layout.addWidget( self.cmb_nivel );
        layout.addWidget( QLabel("Título", self) );
        layout.addWidget( self.titulo);
        layout.addStretch();

    def botao_salvar_conhecimento_click(self):
        self.conhecimento.setHtml( self.editor.toHtml() );
        self.conhecimento.titulo = self.titulo.text();
        self.conhecimento.id_nivel = self.xmpp_var.grupo.niveis[ self.cmb_nivel.currentIndex() ].id;
        self.xmpp_var.adicionar_mensagem("comandos.conhecimento" ,"ConhecimentoComando", "salvar", self.conhecimento.toJson() );
    
    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        self.block_signals(self._format_actions, True)
        self.block_signals(self._format_actions, False)
        