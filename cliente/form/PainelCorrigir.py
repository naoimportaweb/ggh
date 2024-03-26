import time, base64, uuid, os, sys, json, traceback, threading;

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import *
from PySide6 import QtWidgets;
from PySide6.QtCore import *

class PainelCorrigir(QtWidgets.QWidget):
    def __init__( self, xmpp_var ):
        super().__init__();
        self.xmpp_var = xmpp_var;
        self.ativo = False;
        self.layout_carregado = False;
        
    def atualizar_tela(self):
        if self.layout_carregado:
            return;
        self.layout_carregado = True;
    def evento_mensagem(self, de, texto, message, conteudo_js):
        print();