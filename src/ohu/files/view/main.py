from gizmo.vimo import view
from gizmo.utils import tag

from .mixin import Locate

class FilesView(
        Locate,
        view.mixin.TreeGo,
        view.mixin.TreeMove,
        view.TreeView
        ):

    prefix_keys={
        'command': 'f', 
        '|FilesView': '<c-.>'}
    position={'FilesView': 'dock_left'}

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    @tag('o', modes=['normal|FilesView'])
    def open(self):
        raise

    @tag(modes=['exec'])
    def openFile(self):
        raise

    def setModel(self, model):

        if model:
            super().setModel(model)
            for i in range(1, 4): 
                self.hideColumn(i)

    def setSource(self, source):

        m=self.m_model
        if m:
            idx=m.getPathIndex(source)
            pidx=idx.parent()
            self.setRootIndex(pidx)
            self.expand(idx)

    def setPath(self, path=None):

        m=self.m_model
        idx=m.getPathIndex(path)
        self.setRootIndex(idx)
