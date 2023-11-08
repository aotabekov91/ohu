import fitz
from PyQt5 import QtCore, QtGui

class Outline:

    hasOutline=True

    def setup(self):

        super().setup()
        self.m_outline=QtGui.QStandardItemModel()

    def getOutline(self):
        return self.m_outline

    def setModel(self, model):

        super().setModel(model)
        model.loaded.connect(
                self.setOutline)

    def setOutline(self):

        o=self.m_model.m_data.outline
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
            # page = o.dest.ld.gotor.page + 1
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

    def openOutlineItem(self, oitem):

        p=oitem.data()
        self.goto(p)

    def findInOutline(self, vitem):

        if vitem:
            m=self.m_outline
            idx=vitem.element().index()
            goto=0
            for r in range(m.rowCount()):
                if idx<m.item(r).data():
                    return m.index(goto, 0)
                goto=r
