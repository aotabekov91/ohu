from PyQt5 import QtCore
from ohu.base.view import View as Base

from .item import Item
from .cursor import Cursor

class View(Base):

    def __init__(self, *args, **kwargs):

        kwargs['item_class']=Item
        kwargs['cursor_class']=Cursor
        super().__init__(*args, **kwargs)

    def prepareView(self, x=0, y=0, p=0):

        vv, hv = 0, 0
        s = self.scene()
        r = s.sceneRect()
        l, t = r.left(), r.top()
        w, h = r.width(), r.height()
        for j, i in enumerate(self.m_items):
            pbr = i.boundingRect()
            pos = pbr.translated(i.pos())
            c=self.s_settings.get(
                    'continuousMode', True)
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
            if j == p:
                hv = int(pos.left()+x*pos.width())
                vv = int(pos.top()+y*pos.height())

        self.setSceneRect(l, t, w, h)
        self.horizontalScrollBar().setValue(hv)
        self.verticalScrollBar().setValue(vv)
        self.viewport().update()

    def prepareScene(self, w, h):

        items=self.getItems()
        for i in items:
            x=self.logicalDpiX()
            y=self.logicalDpiY()
            i.setResolution(x, y)
            dw= i.displayedWidth()
            dh = i.displayedHeight()
            fitPageSize=[w/float(dw), h/float(dh)]
            width_ratio=w/dw
            scale = {
                'ScaleFactor': i.scale(),
                'FitToWindowWidth': width_ratio,
                'FitToWindowHeight': min(fitPageSize)
                }
            s=scale[self.s_settings.get(
                'scaleMode', 
                'FitToWindowHeight'
                )]
            i.setScaleFactor(s)
        h = self.s_settings.get('pageSpacing', 0.0)
        l, r, h = self.m_layout.load(items, height=h)
        self.scene().setSceneRect(l, 0.0, r-l, h)

    def goto(
            self, 
            digit=None, 
            x=0., 
            y=0.
            ):

        c = self.count() 
        x, y = self.getPosition()
        p = digit or c 
        p-=1
        if 0 <= p < c:
            cp=self.m_layout.current(p)
            c = self.m_curr != cp 
            c = any([c, abs(x-x) > 0.001])
            c = any([c, abs(y-y) > 0.001])
            if c:
                self.prepareView(x, y, p)
                self.setVisiblePage()

    def cleanUp(self):

        super().cleanUp()
        for i in self.getItems(): 
            i.select()
            i.setSearched()

    def initialize(self):

        super().initialize()
        self.fitToWindowWidth()

    def yank(self):

        selected=self.selected()
        if selected: 
            t=[]
            for s in selected: 
                t+=[s['text']]
            clip=self.app.uiman.qapp.clipboard()
            clip.setText(' '.join(t))
            self.select()
            self.refresh()
