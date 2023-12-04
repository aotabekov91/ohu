from gizmo.vimo import view

from . import mixin

class View(
        mixin.Go,
        mixin.Line,
        mixin.Locate,
        mixin.Visual,
        view.ListView,
        ):

    def open(self, **kwargs):

        m=self.m_model
        idx=self.currentIndex()
        path=m.filePath(idx)
        if m.isDir(idx):
            p=idx.parent()
            self.setRootIndex(p)
            self.setCurrentIndex(idx)
        else:
            self.app.handler.handleOpen(
                    path, **kwargs)

    def count(self):

        idx=self.currentIndex()
        pidx=idx.parent()
        return self.m_model.rowCount(pidx)

    def setPath(self, path=None):

        m=self.m_model
        idx=m.getPathIndex(path)
        self.setRootIndex(idx)

    def setSource(self, source):

        m=self.m_model
        idx=m.getPathIndex(source)
        self.setRootIndex(idx.parent())
        self.expand(idx)

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
