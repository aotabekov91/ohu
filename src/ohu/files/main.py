import os
from plug.qt import Plug
from gizmo.utils import tag

from .view import FilesView
from .model import FilesModel

class FileBrowser(Plug):

    def setup(self):

        super().setup()
        self.app.handler.addViewer(
                FilesView)
        self.app.handler.addModeller(
                FilesModel)
        path=os.path.abspath('.')
        self.app.handler.handleInitiate(path)
        self.setArgOptions()

    def setArgOptions(self):

        plugs=self.app.moder.plugs
        p=plugs.get('exec', None)
        if p: 
            p.setArgOptions(
                'openFile', 'path', 'path')

    @tag(modes=['exec'])
    def openFile(self, path):
        self.app.handler.handleOpen(path)
