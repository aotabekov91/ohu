import os
from plug import Plug
from gizmo.vimo import view

from .mixin import Locate

class FileBrowserView(
        Locate,
        view.mixin.TreeGo,
        view.mixin.TreeMove,
        view.TreeView
        ):

    isUnique=True
    pos='dock_left'

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
