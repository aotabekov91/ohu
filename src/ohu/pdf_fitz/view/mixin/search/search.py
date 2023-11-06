from PyQt5 import QtCore
from .task import SearchTask

class Search:

    canSearch=True
    searchFound=QtCore.pyqtSignal(object)

    def setup(self):

        super().setup()
        self.pool=QtCore.QThreadPool()
        self.m_task = SearchTask(self)
        self.m_task.signals.ready.connect(
            self.on_searchReady)
        self.m_task.signals.finished.connect(
            self.on_searchFinished)

    def search(self, text):

        self.m_task.m_text=text
        self.pool.start(self.m_task)

    def on_searchReady(self, data):
        self.searchFound.emit(data)

    def on_searchFinished(self):
        self.m_task.wait=False
