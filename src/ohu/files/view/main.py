import os
from gizmo.vimo import view
from gizmo.utils import tag

from .mixin import Locate

class FilesView(
        Locate,
        view.mixin.TreeGo,
        view.TreeView
        ):

    prefix_keys={
        'command': 'f', 
        '|FilesView': '<c-.>'}
    position={'FilesView': 'dock_left'}

    def setup(self):

        super().setup()
        self.setArgOptions()

    def setArgOptions(self):

        plugs=self.app.moder.plugs
        p=plugs.get('exec', None)
        if p: 
            p.setArgOptions(
                'openFile', 'path', 'path')

    def count(self):

        idx=self.currentIndex()
        pidx=idx.parent()
        return self.m_model.rowCount(pidx)

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    def setPath(self, path=None):

        m=self.m_model
        idx=m.getPathIndex(path)
        self.setRootIndex(idx)

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

    @tag(modes=['exec'])
    def openFile(
            self, 
            path, 
            how=None, 
            horizontal=False,
            **kwargs
            ):

        self.open(
                path, 
                how=how,
                horizontal=horizontal,
                **kwargs
                )

    @tag('o', modes=['normal|FilesView'])
    def open(self, path, **kwargs):

        m=self.m_model
        idx=m.index(path)
        p=idx.parent()
        self.setRootIndex(p)
        self.setCurrentIndex(idx)

    def resetConfigure(
            self, 
            model=None, 
            **kwargs):

        if model:
            s=model.source()
            idx=model.index(s)
            p=idx.parent()
            self.setRootIndex(p)
            self.setCurrentIndex(idx)
