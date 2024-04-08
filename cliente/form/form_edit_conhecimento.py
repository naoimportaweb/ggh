import sys, os, json, base64, re, requests;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QPalette, QFont;
from PySide6.QtCore import Qt;
from PySide6 import QtWidgets;
from PySide6.QtWidgets import QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
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
        self.setWindowTitle("Editar Conhecimento");
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


        
        if self.xmpp_var.cliente.id == conhecimento.id_cliente and conhecimento.id_status == 0:
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
        
        if self.xmpp_var.cliente.posso_tag("aprovador_conhecimento"):
            page_apr = QWidget(tab);
            page_apr_layout = QGridLayout();
            page_apr.setLayout(page_apr_layout);
            tab.addTab(page_apr,'Aprovação');
            self.layout_aprovacao( page_apr_layout,       self.conhecimento);
        
        self.showMaximized() 

    def layout_tag(self, layout, conhecimento):
        layout.addWidget( QLabel("TAGs:", self) );

    def layout_aprovacao(self, layout, conhecimento):
        page = QWidget(self);
        page_layout = QHBoxLayout();
        page.setLayout(page_layout);
        #page_layout.addWidget(label);
        #page_layout.addWidget(self.titulo);
        self.txt_comentario = QTextEdit(self);
        layout.addWidget( self.txt_comentario );

        btn_aprovar = QPushButton("Aprovar")
        btn_aprovar.clicked.connect( self.btn_click_aprovar);
        btn_reprovar = QPushButton("Reprovar")
        btn_reprovar.clicked.connect( self.btn_click_reprovar);
        btn_editar = QPushButton("Editar")
        btn_editar.clicked.connect( self.btn_click_editar);
        btn_reprovar.setStyleSheet("background-color: red;    color: black");
        btn_aprovar.setStyleSheet( "background-color: green;  color: black");
        btn_editar.setStyleSheet(  "background-color: yellow; color: black");
        if self.conhecimento.id_status == 0:
            page_layout.addWidget(btn_aprovar);
            page_layout.addWidget(btn_reprovar);
        elif self.conhecimento.id_status == 1:
            page_layout.addWidget(btn_aprovar);
            page_layout.addWidget(btn_editar);
        elif self.conhecimento.id_status == 2:
            page_layout.addWidget(btn_reprovar);
            page_layout.addWidget(btn_editar);
        layout.addWidget( page );
    
    def mudar_status_conhecimento(self, id_status): # 0 desenv, 1 aguardando, 2 aprovado, 3 reprovado (tabela no banco)
        self.conhecimento.id_status = id_status;
        self.xmpp_var.adicionar_mensagem("comandos.conhecimento" ,"ConhecimentoComando", "alterar_status", self.conhecimento.toJson() );
    def btn_click_aprovar(self):
        self.mudar_status_conhecimento(2);
    def btn_click_reprovar(self):
        self.mudar_status_conhecimento(3);
    def btn_click_editar(self):
        self.mudar_status_conhecimento(0);

    def layout_editor(self, layout, conhecimento):
        # TAB DE TEXTO -> CONHECIMENTO
        self.editor = TextEdit()
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.black);
        palette.setColor(QPalette.Text, Qt.black);
        self.editor.setPalette(palette);
        self.editor.setStyleSheet("background-color: rgb(255, 255, 255);");
        self.editor.setReadOnly(True);

        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)
        font = QFont('Times', 12)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)
        self._format_actions = [ ]
        self.editor.setHtml( conhecimento.texto );
        layout.addWidget( QLabel("Conhecimento", self) );
        layout.addWidget(self.editor)
        if self.conhecimento.id_status == 0:
            widget_botton = QWidget();
            botton_layout = QHBoxLayout();
            widget_botton.setLayout( botton_layout );
            btn_importar_html = QPushButton("Importar HTML");
            btn_importar_html.clicked.connect(self.btn_importar_html_click)
            botton_layout.addWidget( btn_importar_html );
            layout.addWidget(widget_botton);


    def btn_importar_html_click(self):
        dialog = QFileDialog(self)
        dialog.setDirectory('/')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("HTML (*.html *.htm)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles();
            if filenames:
                html = open(filenames[0],"r").read();
                if re.search(r'src="(.*?)"', html) != None:
                    QMessageBox.information(self, "HTML com problemas", "Não pode ter nenhum arquivo anexado.", QMessageBox.StandardButton.Ok);
                if re.search(r'href="(.*?)"', html) != None:
                    QMessageBox.information(self, "HTML com problemas", "Não pode ter nenhum link externo.", QMessageBox.StandardButton.Ok);
                self.editor.setHtml( html );
    
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
        if self.conhecimento.id_status != 0:
            self.titulo.setReadOnly(True);

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
        