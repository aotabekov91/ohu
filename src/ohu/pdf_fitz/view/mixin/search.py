from gizmo.vimo.view.mixin import Search as Base

class Search(Base):

    def on_searchFound(self, e, d):
        print(e, d)

    def search(self, text):

        if self.m_model:
            self.m_model.search(text)
