
import time, traceback;
from PySide6.QtCore import QObject, QThread, Signal, Slot;
from PySide6.QtCore import Qt;
from PySide6.QtWidgets import QWidget
import sys

class MonitorRequestThread(QObject):
    monitor_request_signal = Signal(object);
    def __init__(self, request_id, xmpp_var):
        super().__init__();
        self.request_id = request_id;
        self.xmpp_var = xmpp_var;
    
    @Slot()
    def monitor_request(self):
        while True:
            try:
                #buffer = list(map(lambda x:x if x.id == self.request_id else [], self.xmpp_var.grupo.processados));
                index = -1;
                for i in range(len(self.xmpp_var.grupo.processados)):
                    if self.xmpp_var.grupo.processados[i].id == self.request_id:
                        index = i;
                        break;
                
                if index >= 0:
                    self.monitor_request_signal.emit(self.xmpp_var.grupo.processados.pop(index));
                    break;
            except:
                traceback.print_exc();
                break;
            finally:
                time.sleep(0.3);

class MonitorRequest(QWidget):
    def __init__(self, request_id, xmpp_var, callback):
        super().__init__();
        self.requisicao = MonitorRequestThread(request_id, xmpp_var);
        self.thread = QThread(parent=self);
        self.requisicao.monitor_request_signal.connect(self.montior_callback);
        self.requisicao.moveToThread(self.thread);
        self.thread.started.connect(self.requisicao.monitor_request); 
        self.thread.start();
        self.callback = callback;
    @Slot(object)
    def montior_callback(self, js):
        self.callback(js);
    def quit(self):
        self.thread.quit();