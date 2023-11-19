import os
from gizmo.utils import tag
from plug.qt.plugs.render import Render

from .view import FileBrowserView
from .model import FileBrowserModel

class FileBrowser(Render):

    unique=True
    keywords=['files']
    position='dock_left'
    view_class=FileBrowserView
    model_class=FileBrowserModel
    leader_keys={
        'command': 'f', 
        'FileBrowser': '<c-.>'}

    def isCompatible(self, s):
        return s and os.path.isdir(s)

    def activate(self):

        m=self.app.moder
        self.setView(self.view)
        m.typeWanted.emit(self.view)

    def setup(self):

        super().setup()
        self.model=self.getModel('/')
        self.view=self.getView(self.model)

    def open(self, source, **kwargs):

        self.view.setSource(source)
        self.activate()

    @tag(modes=['run'])
    def openLocalFile(
            self, 
            path, 
            how=None, 
            focus=True
            ):

        self.view.openFile(path, how, focus)
