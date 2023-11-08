from math import ceil
from PyQt5 import QtCore, QtGui

class Hint:

    canHint=True
    hintFinished=QtCore.pyqtSignal()
    hintSelected=QtCore.pyqtSignal(object)

    def setup(self):

        self.m_hint_cache={}
        self.m_hinting_items=[]
        self.clearHint()
        super().setup()

    def hint(self, alist=None):

        vis=self.visibleItems()
        self.m_hinting_items=vis
        if alist is None:
            alist=self.getHintWordList()
        if alist:
            m, mm=self.generate(alist)
            self.m_hint_map=m
            self.m_hint_remap=mm
            self.connectHint()
            self.updateHintItems()
        else:
            self.hintFinished.emit()
            self.cleanUpHinting()

    def updateHintItems(self):

        for i in self.m_hinting_items:
            i.update()

    def connectHint(self):

        for i in self.m_hinting_items:
            i.painted.connect(self.paintHints)

    def disconnectHint(self):

        for i in self.m_hinting_items:
            i.painted.disconnect(self.paintHints)

    def updateHint(self, key=''):

        match={}
        for k, l in self.m_hint_remap.items():
            if key==k[:len(key)]:
                match[k]=l
        if len(match)==0:
            self.hintFinished.emit()
            self.cleanUpHinting()
        elif len(match)==1:
            d=match[list(match.keys())[0]]
            self.hintSelected.emit(d)
            self.cleanUpHinting()
        else:
            hints={}
            for k, (i, d) in match.items():
                if not i  in hints:
                    hints[i]={}
                hints[i][k]=d
            self.m_hint_map=hints
            self.m_hint_remap=match
            self.updateHintItems()

    def cleanUpHinting(self):

        self.disconnectHint()
        self.clearHint()

    def clearHint(self):

        self.m_hint_map={}
        self.m_hint_remap={}
        self.updateHintItems()
        self.m_hinting_items=[]

    def generate(self, alist):

        alpha = 'abcdefghijklmnopqrstuvwxyz'

        def remap(n, l):
            c = []
            for _ in range(l):
                c.append(alpha[n % len(alpha)])
                n = n // len(alpha)
            return "".join(reversed(c))

        hmap={}
        hints={}
        l=0
        al=len(alpha)
        ll=len(alist)
        while al**l<ll: l+=1
        l = max(l, 1)
        for j, d in enumerate(alist):
            item=d['item']
            if not item in hints:
                hints[item]={}
            m=remap(j, l)
            hmap[m]=d
            hints[item][m]=d
        return hints, hmap

    def getHintWordList(self):

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
