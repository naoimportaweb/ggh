import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);

sys.path.append(ROOT);

from classes.singleton.singlegon_meta import SingletonMeta;
from classes.singleton.configuracao import Configuracao;
from classes.conexao.xmpp_client import XMPPCliente;

from api.aeshelp import AesHelper;

from form.login import FormLogin;
from form.painel import FormPainel;
from form.grupo import FormGrupo;

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,  QPalette, QColor;
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow;
from PySide6 import QtWidgets;


class MDIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grupo")
        self.mdiArea = QMdiArea()
        self.setCentralWidget( self.mdiArea )
        bar = self.menuBar()
        file = bar.addMenu("Grupos")

        newAct = QAction('Conectar em um grupo', self)
        file.addAction(newAct)
        newAct.triggered.connect(self.action_connect)

    
    def callback_login(self, xmpp_var):
        form = FormGrupo( self );
        form.set_grupo( xmpp_var );
        sub = self.mdiArea.addSubWindow( form );
        form.showMaximized();
        form.carregar_panel();

    def action_connect(self, q):
        f = FormLogin( self );
        f.exec();
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    #app.setStyle("Fusion")
    #app.setPalette(palette)
    form = MDIWindow()
    form.show()
    sys.exit(app.exec())
    sys.exit(0);







