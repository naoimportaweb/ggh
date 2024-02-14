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
        page_elementos_layout = QGridLayout();
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

        #CREATE TABLE conhecimento ( id varchar(255) NOT NULL, id_cliente varchar(255) NOT NULL, id_revisor varchar(255) DEFAULT NULL,  id_nivel varchar(255) NOT NULL,
        #id_grupo varchar(255) NOT NULL, titulo varchar(255), tags varchar(255), descricao LONGTEXT, texto LONGTEXT, status int not null, 
        # FIM
        self.b5 = QPushButton("Salvar conhecimento")
        self.b5.clicked.connect( self.botao_salvar_conhecimento_click )
        self.main_layout.addWidget(self.b5)
        self.setLayout(self.main_layout);
        self.layout_principal( page_elementos_layout, self.conhecimento);
        self.layout_editor(    page_text_layout,      self.conhecimento);

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
        layout.addWidget(self.editor)

    def layout_principal(self, layout, conhecimento):
        self.titulo = QLineEdit(conhecimento.titulo, self);
        self.cmb_nivel = QComboBox(); 
        self.cmb_nivel.clear();
        if len(self.xmpp_var.grupo.niveis) > 0:
            for nivel in self.xmpp_var.grupo.niveis:
                self.cmb_nivel.addItem(nivel["nome"]);
            self.cmb_nivel.setCurrentIndex(0);
            #self.botao_listar_conhecimento_click();
        
        #index = self.cmb_nivel.findText(conhecimento., QtCore.Qt.MatchFixedString)
        #if index >= 0:
        #     self.cmb_nivel.setCurrentIndex(index)
        layout.addWidget( self.cmb_nivel );
        layout.addWidget( self.titulo);
        layout.addStretch();

    def substituir_url_imagem(self, html, url):
        conteudo_base = base64.b64encode(requests.get(url).content);
        return html.replace( url, "data:image/*;base64," + conteudo_base.decode("utf-8")) ;
    def substituir_url_link(self, html, url):
        partes = re.findall(r'href=[\'|\"](.*?)[\'|\"]', url[0]  );
        if len(partes) > 0:
            html = html.replace('<a'+ url[0] +'>'+ url[1] +'</a>',  striphtml( url[1] ) + " (" + partes[0] + ")" );
        else:
            html = html.replace('<a'+ url[0] +'>'+ url[1] +'</a>', "" );
        return html;
    
    def limpar_tags_indesejadas(self, html):
      scripts = re.compile(r'<(script).*?</\1>(?s)')
      css = re.compile(r'<style.*?/style>')
      a = re.compile(r'<a.*?/a>')
      html = scripts.sub('', html)
      html = css.sub('', html)
      html = a.sub('', html)
      return html;

    def botao_salvar_conhecimento_click(self):
        html = self.editor.toHtml();
        images = re.findall(r'src=[\"|\']([^\"|\']+)[\"|\']', html  );
        images.sort();
        for image in images:
            if image[:len("data:image/*;base64,")] != "data:image/*;base64,":
                html = self.substituir_url_imagem(html, image);
        urls = re.findall(r'<a(.*?)>(.*?)</a>', html  );
        urls.sort();
        for url in urls:
            html = self.substituir_url_link(html, url);
        html = self.limpar_tags_indesejadas(html);
        #with open('/tmp/documento.html', 'w') as yourFile:
        #    yourFile.write( html   )

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        self.block_signals(self._format_actions, True)
        self.block_signals(self._format_actions, False)
        