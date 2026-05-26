

from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;
from PySide6 import QtWidgets;
from PySide6.QtWidgets import QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;

class Table(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent);
        self.lista = [];
        self.total_linhas = 0;
    def cleanList(self):
        self.lista = [];
        self.total_linhas = 0;
        self.setRowCount( 0 );
    def add(self, array_colunas, objeto):
        self.setRowCount( self.total_linhas + 1 );
        for i in range(len(array_colunas)):
            self.setItem( self.total_linhas , i, QTableWidgetItem( array_colunas[i] ) );
        self.lista.append( objeto );
        self.total_linhas += 1;
    def get(self):
        return self.lista[self.currentRow()];
