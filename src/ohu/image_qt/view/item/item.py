from PyQt5 import QtCore, QtGui, QtWidgets
from gizmo.widget.view import RenderMixin, BaseItem

from .tile import Tile

class Item(
        RenderMixin,
        BaseItem,
        QtWidgets.QGraphicsObject
        ):

    def setup(self):

        super().setup()
        if not self.useTiling: 
            tile=Tile(self)
            self.m_tileItems=[tile]
        self.redraw()

    def paintItem(self, p, opts, wids):

        p.fillRect(
                self.m_brect, 
                QtGui.QBrush(QtGui.QColor('white')))
        self.m_tileItems[0].paint(
                p, self.m_brect.topLeft())

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
