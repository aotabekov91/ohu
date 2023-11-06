from gizmo.vimo.model.mixin import Search as Base

from .task import SearchTask

class Search(Base):

    def setup(self):

        self.m_cache={}
        self.m_task = SearchTask(self)
        self.m_task.finished.connect(
            self.on_searchFinished)
        self.m_task.taskReady.connect(
            self.on_searchReady)
        self.m_task.cancel(True)
        self.m_task.wait()
        super().setup()

    def on_searchReady(self, data):
        raise

    def on_searchFinished(self):
        raise

    def reportFromCache(self, cache):
        raise

    def search(self, text):

        self.cancel()
        cached=self.m_cache.get('text', None)
        if cached:
            self.reportFromCache(cached)
        else:
            self.m_task.start(text)

    def cancel(self):

        if self.m_task.isRunning():
            self.m_task.cancel(True)

