from gizmo.vimo import view
from gizmo.utils import tag

from .view import FilesView

class FTab(view.Tabber):

    tab_class=FilesView
    prefix_keys={'command': 'f'}
    position={'FTab': 'dock_left'}
    
    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    def setModel(self, model):

        if not self.current_tab:
            self.tabAddNew()
        self.current_tab.setModel(model)
