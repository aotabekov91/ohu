from PyQt5 import QtCore

class Task(QtCore.QObject, QtCore.QRunnable):

    NotCanceled=0
    CanceledNormally=1
    CanceledForcibly=2

    finished = QtCore.pyqtSignal()
    imageReady = QtCore.pyqtSignal(
            'QRect', bool, 'QImage')

    def __init__(self, parent):

        super().__init__(parent)
        self.m_prefetch = False
        self.m_isRunning = False
        self.m_wasCanceled=self.NotCanceled
        self.m_mutex=QtCore.QMutex()
        self.setup()

    def setup(self):

        self.m_waitCondition=QtCore.QWaitCondition()

    def start(self, rect, prefetch):

        self.m_rect = rect
        self.m_prefetch = prefetch
        self.m_mutex.lock()
        self.m_isRunning = True
        self.m_mutex.unlock()
        self.m_wasCanceled=self.NotCanceled
        self.run()

    def cancel(self, force=False):

        self.m_wasCanceled=self.CanceledNormally
        if force:
            self.m_wasCanceled=self.CanceledForcibly

    def wait(self):
        while self.m_isRunning:
            self.m_waitCondition.wait(self.m_mutex)

    def isRunning(self):
        return self.m_isRunning

    def wasCanceled(self):
        return self.m_wasCanceled!=self.NotCanceled

    def wasCanceledNormally(self):
        return self.m_wasCanceled==self.CanceledNormally

    def wasCanceledForcibly(self):
        return self.m_wasCanceled==self.CanceledForcibly

    def element(self):
        return self.item().element()

    def item(self):
        return self.parent().item()

    def run(self):

        image = self.element().render(
            self.item().scaledResolutionX(),
            self.item().scaledResolutionY(),
            self.item().rotation(),
            self.m_rect)

        image.setDevicePixelRatio(self.item().devicePixelRatio())
        self.imageReady.emit(self.m_rect, self.m_prefetch, image)
        self.finish()

    def finish(self):

        self.finished.emit()
        self.m_mutex.lock()
        self.m_isRunning = False
        self.m_mutex.unlock()
        self.m_waitCondition.wakeAll()
