import time
from PyQt5 import QtCore

class Signals(QtCore.QObject):

    ready = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal()

class SearchTask(QtCore.QRunnable):

    def __init__(self, view):

        self.m_view=view
        self.signals=Signals()
        super().__init__()

    def start(self, text):

        self.m_text=text
        self.run()
        
    @QtCore.pyqtSlot()
    def run(self):

        self.wait=True
        items=self.m_view.getItems()
        for j, i in items:
            e=i.m_element
            f=e.search(self.m_text)
            self.reportFound(i, f)
        self.signals.finished.emit()
        while self.wait:
            time.sleep(0.01)

    def reportFound(self, i, found):

        if found: 
            data=[]
            for f in found:
                x, y = f.x0, f.y0
                w, h = f.width, f.height 
                p=(x, y, w, h)
                pe=i.mapToElement(p, unify=True)
                data+=[(i, pe)]
            self.signals.ready.emit(data)
