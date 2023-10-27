from PyQt5 import QtCore, QtGui, QtWidgets
from gizmo.ui.view.item import Item as Base

from .tile import Tile

class Item(Base):

    def setup(self):

        super().setup()
        if not self.useTiling: 
            tile=Tile(self)
            self.m_tileItems=[tile]
        self.redraw()

    def setupPaint(self, p, opts, wids):

        super().setupPaint(p, opts, wids)
        self.paintSearch(p, opts, wids)
        self.paintSelection(p, opts, wids)

    def paintItem(self, p, opts, wids):

        p.fillRect(
                self.m_brect, 
                QtGui.QBrush(QtGui.QColor('white')))
        self.m_tileItems[0].paint(
                p, self.m_brect.topLeft())

    def paintSelection(self, p, opts, wids):

        p.save()
        s=self.m_view.selected() or []
        for i in s:
            if self==i['item']: 
                b=i['box']
                a=[self.mapToItem(b) for b in b]
                b=QtGui.QBrush(self.select_bcolor)
                p.setBrush(self.select_bcolor)
                p.drawRects(a)
                pen=QtGui.QPen(self.select_pcolor, 0.0)
                p.setPen(pen)
                p.drawRects(a)
        p.restore()

    def paintSearch(self, p, opts, wids):

        if len(self.m_searched)>0:
            p.save()
            p.setPen(QtGui.QPen(QtCore.Qt.red, 0.0))
            p.drawRects(self.m_searched)
            p.restore()

    def select(self, selections=[]):

        for s in selections:
            box=s['box']
            s['item']=self
            s['area_item']=[]
            s['area_unified']=[]
            for b in box:
                s['area_item']+=[self.mapToItem(b)]
                s['area_unified']+=[self.mapToPage(
                    b, unify=True)]
        self.m_view.select(selections)
        self.update()

    def prepareGeometry(self):

        super().prepareGeometry()
        self.prepareTiling()

    def refresh(self, dropCache=False):

        for tile in self.m_tileItems:
            tile.refresh(dropCache)
            if dropCache: 
                tile.dropCaches(self)
        super().refresh(dropCache)

    def prepareTiling(self):

        br=self.m_brect
        w, h=int(br.width()), int(br.height())
        r=QtCore.QRect(0, 0, w, h)
        self.m_tileItems[0].setRect(r)

    def startRender(self, prefetch):
        
        for tile in self.m_tileItems:
            tile.startRender(prefetch)

    def cancelRender(self):

        for tile in self.m_tileItems:
            tile.cancelRender()
