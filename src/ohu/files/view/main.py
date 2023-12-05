from gizmo.vimo import view
from gizmo.utils import tag

from .view import FilesView

class FTab(view.Tabber):

    tab_class=FilesView
    prefix_keys={'command': 'f'}
    position={'FTab': 'dock_left'}

    def tabAddNew(self, copy=False):

        ptab=self.current_tab
        if ptab:
            ntab=ptab.copy()
        else:
            ntab=self.tabGet()
        self.tabAdd(ntab)
        self.tabSet(ntab)
        self.setFocus()
        return ntab
    
    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    def setModel(self, model):

        if not self.current_tab:
            self.tabAddNew()
        self.current_tab.setModel(model)
