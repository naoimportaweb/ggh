
import sys, os, json, base64, re, requests;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import *
#from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QTabWidget, QVBoxLayout, QGridLayout,  QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QFormLayout, QLabel, QMessageBox;
from PySide6 import QtWidgets;
from PySide6.QtWidgets import *
from PySide6.QtCore import *

# https://www.pythonguis.com/examples/python-rich-text-editor/
class TextEdit(QTextEdit):
    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def createMimeDataFromSelection(self):
        cursor = self.textCursor()
        if len(cursor.selectedText()) == 1:
            cursor.setPosition(cursor.selectionEnd())
            fmt = cursor.charFormat()
            if fmt.isImageFormat():
                url = QUrl(fmt.property(fmt.ImageName))
                image = self.document().resource(
                    QTextDocument.ImageResource, url)
                mime = QMimeData()
                mime.setImageData(image)
                return mime
        return super().createMimeDataFromSelection()

    def insertImage(self, image):
        if image.isNull():
            return False
        if isinstance(image, QPixmap):
            image = image.toImage()
        doc = self.document()
        if image.width() > doc.pageSize().width():
            image = image.scaledToWidth(int(doc.pageSize().width()), 
                Qt.SmoothTransformation)
        ba = QByteArray()
        buffer = QBuffer(ba)
        image.save(buffer, 'PNG', quality=95)
        binary = base64.b64encode(ba.data())
        HTMLBin = "<img src= \"data:image/*;base64,{}\" ></img>".format(
            str(binary, 'utf-8'))
        self.textCursor().insertHtml(HTMLBin)
        return True

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        document = self.document()
        if source.hasUrls():
            for url in source.urls():
                path = url.toLocalFile();
                info = QFileInfo(path);
                self.insertImage(QImage(path));
                return;
        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image);
            self.insertImage(QImage(path));
            return;
        else:
            print(source);
        super(TextEdit, self).insertFromMimeData(source)


