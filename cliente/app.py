import sys, os, inspect, time, json;
import threading

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);

sys.path.append(ROOT);

from classes.singleton.singlegon_meta import SingletonMeta;
from classes.singleton.configuracao import Configuracao;
from classes.conexao.xmpp_client import XMPPCliente;

#from api.aeshelp import AesHelper;

from form.form_login  import FormLogin;
from form.form_login_importar import FormImportar;
from form.form_painel import FormPainel;
from form.form_grupo  import FormGrupo;
from form.form_edit_conhecimento import FormEditarConhecimento

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,  QPalette, QColor;
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QStatusBar, QLabel;
from PySide6 import QtWidgets;


class MDIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grupo")
        self.mdiArea = QMdiArea()
        self.setCentralWidget( self.mdiArea )
        bar = self.menuBar()
        file = bar.addMenu("Grupos")
        self.statusbar = StatusClass( self );
        newAct = QAction('Conectar em um grupo com login', self);
        file.addAction(newAct);
        newAct.triggered.connect(self.action_connect);
        newAct2 = QAction('Conectar em um grupo com chave', self);
        file.addAction(newAct2);
        newAct2.triggered.connect(self.action_connect_key);
    
    def callback_import_login(self, xmpp_var):
        form = FormGrupo( self );
        xmpp_var.dados = json.loads( open(ROOT + "/data/versao.json", "r").read() );
        form.set_grupo( xmpp_var );
        self.statusbar.adicionar( xmpp_var.grupo );
        sub = self.mdiArea.addSubWindow( form );
        form.showMaximized();
        form.carregar_panel();

    def callback_login(self, xmpp_var):
        form = FormGrupo( self );
        xmpp_var.dados = json.loads( open(ROOT + "/data/versao.json", "r").read() );
        form.set_grupo( xmpp_var );
        self.statusbar.adicionar( xmpp_var.grupo );
        sub = self.mdiArea.addSubWindow( form );
        form.showMaximized();
        form.carregar_panel();

    def action_connect(self, q):
        f = FormLogin( self );
        f.exec();
    def action_connect_key(self):
        f = FormImportar(self);
        f.exec();

class StatusClass():
    def __init__(self, layout):
        self.statusbar = QStatusBar()
        self.statusbar.showMessage("Carregando...", 2000)
        self.wcLabel = QLabel("...")
        self.statusbar.addPermanentWidget(self.wcLabel)
        self.btn_historico = QPushButton("Histórico");
        self.statusbar.addPermanentWidget( self.btn_historico );
        layout.setStatusBar(self.statusbar);
        self.grupos = [];
        x = threading.Thread(target=self.atualizar)
        x.start();

    def adicionar(self, grupo):
        self.grupos.append(grupo);

    def atualizar(self):
        while True:
            try:
                if len(self.grupos) > 0:
                    total = 0;
                    for grupo in self.grupos:
                        if grupo == None or grupo.aguardando_resposta == None or grupo.message_list_send == None:
                            continue;
                        total = total + len(grupo.aguardando_resposta) + len(grupo.message_list_send);
                    self.wcLabel.setText("Pendente: " + str(total)  )
                    #self.wcLabel.repaint();
            finally:
                time.sleep(1);

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
    app.setStyle("Fusion")
    app.setPalette(palette)
    form = MDIWindow()
    form.show()
    sys.exit(app.exec())







