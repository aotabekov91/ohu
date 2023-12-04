from gizmo.vimo import view
from gizmo.utils import tag

from . import mixin

class FilesView(
        # mixin.Hint,
        mixin.Line,
        mixin.Go,
        mixin.Locate,
        mixin.Visual,
        view.ListView,
        # view.mixin.ViewGo,
        ):


    prefix_keys={
        'command': 'f', 
        '|FilesView': '<c-.>'}
    position={'FilesView': 'dock_left'}

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    @tag('o', modes=['normal|FilesView'])
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
