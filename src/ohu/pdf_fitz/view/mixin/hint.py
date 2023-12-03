from PyQt5 import QtCore, QtGui
from gizmo.vimo.view import mixin

class Hint(mixin.Hint):

    def setup(self):

        self.m_hinting_items=[]
        super().setup()

    def hint(self, alist=None, kind=None):

        vis=self.visibleItems()
        self.m_hinting_items=vis
        if kind=='words':
            alist = self.getHintWordsList()
        super().hint(
                alist=alist, kind=kind)

    def connectHint(self):

        for i in self.m_hinting_items:
            i.painted.connect(self.paintHints)

    def disconnectHint(self):

        for i in self.m_hinting_items:
            i.painted.disconnect(self.paintHints)

    def updateHintItems(self):

        for i in self.m_hinting_items:
            i.update()

    def clearHint(self):

        super().clearHint()
        self.updateHintItems()
        self.m_hinting_items=[]

    def getHintWordsList(self):

        alist=[]
        for i in self.m_hinting_items:
            if i in self.m_hint_cache:
                tl=self.m_hint_cache[i]
            else:
                tp=i.element().data().get_textpage()
                tl=[]
                for t in tp.extractWORDS():
                    r=self.createRect(t)
                    r=i.mapToElement(r, unify=True)
                    tl+=[{'item': i, 'box': [r]}]
                self.m_hint_cache[i]=tl
            alist+=tl
        return alist 

    def createRect(self, d):

        tl = QtCore.QPointF(d[0], d[1])
        br = QtCore.QPointF(d[2], d[3])
        return QtCore.QRectF(tl, br)

    def paintHints(self, p, o, w, i):

        if self.m_hinting:
            p.save()
            pen=QtGui.QPen(QtCore.Qt.red, 0.0)
            p.setPen(pen)
            m=self.m_hint_map.get(i, {})
            for j, d in m.items():
                b=d['box']
                if type(b)==list: b=b[0]
                tr=i.mapToItem(b, unified=True)
                p.drawText(tr.topLeft(), j)
            p.restore()
