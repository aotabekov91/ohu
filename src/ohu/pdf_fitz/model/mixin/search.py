from gizmo.vimo.model.mixin import Search as Base

from .task import SearchTask

class Search(Base):

    def search(self, text):

        t=SearchTask(self, text)
        t.searchFound.connect(
                self.searchFound)
        t.start()
