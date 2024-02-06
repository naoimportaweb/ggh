import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QFormLayout, QLabel, QMessageBox;
from PySide6 import QtWidgets;

from classes.conexao.xmpp_client import XMPPCliente;
from classes.conexao.sessao import Sessao;

class FormLogin(QDialog):
    def __init__(self, parent=None):
        super(FormLogin, self).__init__(parent)
        self.setWindowTitle("Grupo")
        self.setGeometry(400, 400, 800, 500)

        self.form_main = parent;
        self.jid_grupo = QLineEdit('', self);
        self.jid_pessoa = QLineEdit('', self);
        self.chave_criptografia = QLineEdit('', self);
        self.password = QLineEdit('', self);

        if os.path.exists(os.path.expanduser("~/.ggh_cliente_desenv.json")):
            buffer_config = json.loads( open(os.path.expanduser("~/.ggh_cliente_desenv.json"), 'r').read() );
            self.jid_grupo.setText( buffer_config["jid_grupo"] );
            self.jid_pessoa.setText( buffer_config["jid_pessoa"] );
            self.chave_criptografia.setText( buffer_config["chave_criptografia"] );
            self.password.setText( buffer_config["password"] );

            buffer_config = None;


        self.chave_criptografia.setEchoMode(QLineEdit.Password)
        self.password.setEchoMode(QLineEdit.Password)

        self.pushButton = QPushButton("Entrar"); 
        self.pushButton.clicked.connect(self.action_btn_entrar) 

        layout = QFormLayout();
        layout.addRow(QLabel("XMPP do grupo"), self.jid_grupo);
        layout.addRow(QLabel("XMPP do participante"), self.jid_pessoa);
        layout.addRow(QLabel("Senha do XMPP do participante"), self.password);
        layout.addRow(QLabel("Chave de criptografia"), self.chave_criptografia);
        layout.addRow(self.pushButton);
        self.setLayout(layout);
        
    
    def action_btn_entrar(self):
        self.pushButton.setEnabled( False );
        xmpp_var = XMPPCliente(self.jid_pessoa.text(), self.password.text(), self.jid_grupo.text(), self.chave_criptografia.text() );
        if xmpp_var.conectar():
            self.form_main.callback_login( xmpp_var );
            self.close();
        else:
            self.pushButton.setEnabled( True );
            QMessageBox.information(self, "Falha de autenticação", "Não foi possível autenticar no serviço XMPP do participante, confirme que seu usuário XMPP está correto e que a senha também esteja correta.", QMessageBox.StandardButton.Ok);