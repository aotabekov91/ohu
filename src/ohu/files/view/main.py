from gizmo.vimo import view
from gizmo.utils import tag

from .view import FilesView

class FTab(view.Tabber):

    canFollow=True
    tab_class=FilesView
    prefix_keys={'command': 'f'}
    position={'FTab': 'dock_left'}

    def tabAddNew(self, copy=False):
        super().tabAddNew(copy=True)

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()
