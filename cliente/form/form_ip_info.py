import sys, os, json;

sys.path.append("../"); # estamos em /form, 

#from PySide6.QtGui import *
from PySide6.QtWidgets import    QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

from form.funcoes import Utilitario;
from api.iplocation import IP;
class FormIPInfo(QDialog):
    def __init__(self, parent=None):
        super(FormIPInfo, self).__init__(parent)
        self.setWindowTitle("Dados de Localização")
        self.setGeometry(400, 400, 800, 500)
        self.form_main = parent;
        self.main_layout = QVBoxLayout( self );      
        self.continuar = False;  
        self.setLayout(self.main_layout);
        ip = IP();
        js = ip.ip_info() ;
        #widget_linha(form, layout, controls, stretch_inicio=False, stretch_fim=False):
        Utilitario.widget_linha( self, self.main_layout, [QLabel("<b>IP      </b>"), QLabel( js["YourFuckingIPAddress"]    )], stretch_fim=True );
        Utilitario.widget_linha( self, self.main_layout, [QLabel("<b>País    </b>"), QLabel( js["YourFuckingCountry"]      )], stretch_fim=True );
        Utilitario.widget_linha( self, self.main_layout, [QLabel("<b>Cidade  </b>"), QLabel( js["YourFuckingCity"]         )], stretch_fim=True );
        Utilitario.widget_linha( self, self.main_layout, [QLabel("<b>Local   </b>"), QLabel( js["YourFuckingLocation"]     )], stretch_fim=True );
        Utilitario.widget_linha( self, self.main_layout, [QLabel("<b>ISP     </b>"), QLabel( js["YourFuckingISP"]          )], stretch_fim=True );
        Utilitario.widget_linha( self, self.main_layout, [QLabel("<b>TOR     </b>"), QLabel(  "Sim" if js["YourFuckingTorExit"] == True else "Não"       )], stretch_fim=True );
        self.main_layout.addStretch();
        btn_continuar = QPushButton("CONTINUAR")
        btn_continuar.clicked.connect( self.btn_click_continuar);
        btn_nao_continuar = QPushButton("Não entrar")
        btn_nao_continuar.clicked.connect( self.btn_click_nao_continuar);
        btn_nao_continuar.setStyleSheet("background-color: red;    color: black");
        btn_continuar.setStyleSheet(    "background-color: green;  color: black");
        Utilitario.widget_linha( self, self.main_layout, [btn_nao_continuar,btn_continuar], stretch_inicio=True );
    def btn_click_continuar(self):
        self.continuar = True; 
        self.close();
    def btn_click_nao_continuar(self):
        self.continuar = False; 
        self.close();
