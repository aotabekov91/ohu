from PyQt5 import QtWidgets
from gizmo.widget.view import (
        DirMixin, 
        XYMixin, 
        ItemMixin, 
        BaseView)

from .item import ImageQtItem

class ImageQtView(
        DirMixin, 
        XYMixin, 
        ItemMixin,
        BaseView,
        QtWidgets.QGraphicsView
        ):

    position='display'
    item_class=ImageQtItem

    def initialize(self):

        super().initialize()
        self.fitToWindowWidth()

    def prepareView(self, digit=1, x=0, y=0):

        vv, hv = 0, 0
        s = self.scene()
        r = s.sceneRect()
        l, t = r.left(), r.top()
        w, h = r.width(), r.height()
        for j, i in self.m_items.items():
            if j!=digit:
                i.setVisible(False)
            else:
                i.setVisible(True)
                pbr = i.boundingRect()
                pos = pbr.translated(i.pos())
                t, h =pos.top(), pos.height()
                hv = int(pos.left()+x*pos.width())
                vv = int(pos.top()+y*pos.height())
                self.setSceneRect(l, t, w, h)
                self.horizontalScrollBar().setValue(hv)
                self.verticalScrollBar().setValue(vv)
                self.viewport().update()
