import os
from plug.qt import Plug
from gizmo.utils import tag

from .view import FTab
from .model import FModel

class FileBrowser(Plug):

    def setup(self):

        super().setup()
        h=self.app.handler
        path=os.path.abspath('.')
        h.addViewer(FTab)
        h.addModeller(FModel)
        h.handleInitiate(path)
        self.setArgOptions()

    def setArgOptions(self):

        plugs=self.app.moder.plugs
        p=plugs.get('exec', None)
        if not p: return
        p.setArgOptions(
            'openFile', 'path', 'path')

    @tag(modes=['exec'])
    def openFile(self, path):
        self.app.handler.handleOpen(path)
