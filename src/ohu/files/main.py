import os
from gizmo.utils import tag
from plug.qt.plugs.render import Render

from .view import FileBrowserView
from .model import FileBrowserModel

class FileBrowser(Render):

    unique=True
    view_class=FileBrowserView
    model_class=FileBrowserModel
    position={'ui': 'dock_left'}
    leader_keys={
        'command': 'f', 
        'FileBrowser': '<c-.>'
        }

    def isCompatible(self, s):
        return s and os.path.isdir(s)

    def activate(self):

        m=self.app.moder
        self.setView(self.m_view)
        m.typeWanted.emit(self.m_view)

    def setup(self):

        super().setup()
        self.m_model=self.getModel('/')
        self.m_view=self.getView(
                self.m_model)

    def open(self, source, **kwargs):

        self.m_view.setSource(source)
        self.activate()

    @tag(modes=['run'])
    def openLocalFile(
            self, 
            path, 
            how=None, 
            focus=True
            ):

        self.m_view.openFile(
                path, how, focus)
