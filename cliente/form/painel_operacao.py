import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import  QGridLayout, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;
from PySide6 import QtWidgets;
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;

#from classes.operacao import Operacao;

class PainelOperacao(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        form_layout = QVBoxLayout( self );
    def evento_mensagem(self, de, texto, message, conteudo_js):
        return;
    def atualizar_tela(self):
        return;