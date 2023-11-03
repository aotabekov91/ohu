from PyQt5 import QtWidgets
from gizmo.widget.view import XYMixin, ItemMixin, BaseView

from .item import DjvuItem

class DjvuView(
        XYMixin,
        ItemMixin,
        BaseView,
        QtWidgets.QGraphicsView,
        ):

    position='display'
    item_class=DjvuItem

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
            pbr = i.boundingRect()
            pos = pbr.translated(i.pos())
            c=self.continuousMode
            if c: 
                i.setVisible(True)
            else:
                if self.m_layout.left(j) == self.m_curr:
                    i.setVisible(True)
                    t = pos.top()
                    h = pos.height()
                else:
                    i.setVisible(False)
                    i.cancelRender()
            if j == digit:
                hv = int(pos.left()+x*pos.width())
                vv = int(pos.top()+y*pos.height())

        self.setSceneRect(l, t, w, h)
        self.horizontalScrollBar().setValue(hv)
        self.verticalScrollBar().setValue(vv)
        self.viewport().update()
