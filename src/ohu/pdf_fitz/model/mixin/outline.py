import fitz
from PyQt5 import QtCore, QtGui
from gizmo.vimo.model import SModel 

class OutlineModel(SModel):

    wantUniqView=True
    wantView=['OutlineView']

class Outline:

    hasOutline=True

    def setup(self):

        super().setup()
        self.m_outline=OutlineModel()
        self.loaded.connect(self.setOutline)

    def getOutline(self):
        return self.m_outline

    def setOutline(self):

        o=self.m_data.outline
        r=self.m_outline.invisibleRootItem()
        self.loadOutline(o, r)

    def loadOutline(self, o, p):

        if not o: 
            return
        t=o.title
        i = QtGui.QStandardItem(t)
        i.setFlags(
                QtCore.Qt.ItemIsEnabled | 
                QtCore.Qt.ItemIsSelectable
                )
        if o.dest.kind != fitz.LINK_NONE:
            # page = o.dest.ld.goTor.page + 1
            page = o.dest.page + 1
            i.setData(page)#, QtCore.Qt.UserRole + 1)
            pi = i.clone()
            pi.setText(str(page))
            pi.setTextAlignment(QtCore.Qt.AlignRight)
            p.appendRow([i, pi])
        else:
            p.appendRow(i)
        if o.next != 0:
            self.loadOutline(o.next, p)
        if o.down != 0:
            self.loadOutline(o.down, i)
