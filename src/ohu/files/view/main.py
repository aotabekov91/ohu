from gizmo.vimo import view
from gizmo.utils import tag

from .view import View

class FilesView(view.Tabber):

    tab_class=View
    prefix_keys={
        'command': 'f', 
        '|FilesView': '<c-.>'}
    position={'FilesView': 'dock_left'}

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    # def setSource(self, source):

    #     m=self.m_model
    #     idx=m.getPathIndex(source)
    #     self.setRootIndex(idx.parent())
    #     self.expand(idx)

    # def resetConfigure(
    #         self, 
    #         model=None, 
    #         **kwargs):

    #     if model:
    #         s=model.source()
    #         idx=model.index(s)
    #         p=idx.parent()
    #         self.setRootIndex(p)
    #         self.setCurrentIndex(idx)
