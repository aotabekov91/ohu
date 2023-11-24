from plug.qt import Plug

from .view import FilesView
from .model import FilesModel

class FileBrowser(Plug):

    def setup(self):

        super().setup()
        self.app.handler.addViewer(
                FilesView)
        self.app.handler.addModeller(
                FilesModel)
        self.app.handler.handleInitiate('/')

    # @tag('t', modes=['command']) 
    # def activate(self):
    #     m=self.app.moder
    #     self.setView(self.m_view)
    #     m.typeWanted.emit(self.m_view)

    # def setup(self):
    #     super().setup()
    #     self.m_model=self.getModel('/')
    #     self.m_view=self.getView(
    #             self.m_model)

    # def open(self, source, **kwargs):
    #     self.m_view.setSource(source)
    #     self.activate()

    # @tag(modes=['run'])
    # def openLocalFile(
    #         self, 
    #         path, 
    #         how=None, 
    #         focus=True
    #         ):
    #     self.m_view.openFile(
    #             path, how, focus)
