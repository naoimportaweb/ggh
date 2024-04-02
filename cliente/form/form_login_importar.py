import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import *

from classes.conexao.xmpp_client import XMPPCliente;
from api.fsseguro import FsSeguro;
from classes.grupo import Grupo;

class FormImportar(QDialog):
    def __init__(self, parent=None):
        super(FormImportar, self).__init__(parent)
        #self.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.15);")
        self.setWindowTitle("Grupo")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.main_layout = QVBoxLayout( );
        
        widget0 = QWidget(self);
        widget0_layout = QHBoxLayout();
        widget0.setLayout( widget0_layout );
        label0 = QLabel("Chave de descriptografia");
        self.txt_chave = QLineEdit('', self);
        self.txt_chave.setEchoMode(QLineEdit.Password)
        widget0_layout.addWidget( label0 );
        widget0_layout.addWidget( self.txt_chave );
        self.main_layout.addWidget( widget0 );

        self.protocolo_proxy = QLineEdit('http', self);
        self.servidor_proxy = QLineEdit('127.0.0.1', self);
        self.porta_proxy = QLineEdit('9051', self);

        layout = QFormLayout();
        layout.addRow(QLabel("Protocolo proxy"), self.protocolo_proxy);
        layout.addRow(QLabel("IP do proxy"),     self.servidor_proxy);
        layout.addRow(QLabel("Porta do Proxy"),  self.porta_proxy);
        widget2 = QWidget();
        widget2.setLayout( layout );
        self.main_layout.addWidget( widget2 );

        widget1 = QWidget(self);
        widget1_layout = QHBoxLayout();
        widget1.setLayout( widget1_layout );
        btn_gerar_imagem = QPushButton("Importar arquivo")
        btn_gerar_imagem.clicked.connect(self.btn_importar_chave); 
        widget1_layout.addStretch();
        widget1_layout.addWidget( btn_gerar_imagem );
        self.main_layout.addWidget( widget1 );

        
        self.setLayout(self.main_layout);
    
    def arquivo(self, filtro="HTML (*.html *.htm)"):
        dialog = QFileDialog(self)
        dialog.setDirectory('/')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter(filtro)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles();
            if filenames:
                return filenames[0];
            else:
                return None;
    
    def btn_importar_chave(self):
        chave = self.txt_chave.text();
        fs = FsSeguro( chave );
        path_file_key = self.arquivo(filtro="Key File (*.gif)");
        js = fs.ler_json( path_file_key );

        grupo = Grupo( js["jid_grupo"] );
        grupo.importar_cliente( js ) ;

        xmpp_var = XMPPCliente( js["jid"], js["password"], js["jid_grupo"], chave );
        if xmpp_var.proxy( self.protocolo_proxy.text() , self.servidor_proxy.text() , self.porta_proxy.text() ):
            if xmpp_var.conectar():
                self.form_main.callback_import_login( xmpp_var );
                self.close();
            else:
                QMessageBox.information(self, "Falha de autenticação", "Não foi possível autenticar no serviço XMPP do participante, confirme que seu usuário XMPP está correto e que a senha também esteja correta.", QMessageBox.StandardButton.Ok);
        else:
            QMessageBox.information(self, "Proxy não existe", "O proxy não funcionou, veja o manual.", QMessageBox.StandardButton.Ok);