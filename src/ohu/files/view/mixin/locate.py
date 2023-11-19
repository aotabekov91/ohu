import os
from gizmo.utils import tag
from gizmo.vimo.view import mixin

class Locate(mixin.Locate):

    def open(self, source=None, **kwargs):

        pos=kwargs.get('position', None)
        path = pos or source
        if self.app.running:
            self._open(path)
        else:
            f=lambda : self._open(path, True)
            self.app.uiman.appLaunched.connect(f)

    def _open(
            self, 
            path, 
            fullscreen=False,
            ):

        m=self.ui.model()
        idx=m.index(path)
        p=idx.parent()
        self.ui.setRootIndex(p)
        self.ui.setCurrentIndex(idx)
        self.activate()
        if fullscreen:
            self.ui.dock.toggleFullscreen()

    @tag('o')
    def openFile(
            self, 
            path=None, 
            how=None, 
            focus=False
            ):

        if not path:
            idx=self.ui.currentIndex()
            path=self.getPath(idx)
        if path:
            if os.path.isdir(path): 
                idx=self.ui.currentIndex()
                self.ui.expand(idx)
            else:
                self.app.open(
                        path, 
                        how=how, 
                        focus=focus)
                self.listen()
