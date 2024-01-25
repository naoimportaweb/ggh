
from PySide6.QtGui import QAction;
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QHBoxLayout;
from PySide6 import QtWidgets;

class FormGrupo(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs);
        self.mdiArea = QMdiArea()
        self.form_layout = QHBoxLayout( self );
        self.form_layout.addWidget( self.mdiArea );
    
    def set_grupo(self, xmpp_var):
        self.xmpp_var = xmpp_var;
        self.xmpp_var.set_callback(self.evento_mensagem);
        self.setWindowTitle( xmpp_var.grupo.jid );
        self.xmpp_var.atualizar_entrada();

    def evento_mensagem(self, de, texto):
        print("RECEBIDO HTML", texto);
    
    def __del__(self):
    	self.xmpp_var.disconnect();
    	self.xmpp_var = None;