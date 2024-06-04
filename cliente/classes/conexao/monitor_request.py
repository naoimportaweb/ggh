

class MonitorRequestThread(QObject):
    image_signal = QtCore.pyqtSignal(js);
    def __init__(self, request_id):
        self.request_id = request_id;
    
    @QtCore.pyqtSlot()
    def monitor_request(self, request_id):
        while True:
            self.image_signal.emit({"id" : request_id});

class MonitorRequest(QtGui.QWidget):
    def __init__(self, request_id)
        self.file_monitor = MonitorRequestThread(request_id);
        self.thread = QtCore.QThread(self);
        self.file_monitor.image_signal.connect(self.montior_callback);
        self.file_monitor.moveToThread(self.thread);
        self.thread.started.connect(self.file_monitor.monitor_request); 
        self.thread.start();

    @QtCore.pyqtSlot(js)
    def montior_callback(self, js):
        print(js);