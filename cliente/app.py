import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("My Form")

class MDIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDI Application")
        mdiArea = QMdiArea()
        self.setCentralWidget( mdiArea )
        bar = self.menuBar()
        file = bar.addMenu("APT")

        newAct = QAction('Connect', self)
        file.addAction(newAct)
        newAct.triggered.connect(self.windowaction)
    
    def action_connect(self, q):
        print("abrir tela de conexão")

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = MDIWindow()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())

