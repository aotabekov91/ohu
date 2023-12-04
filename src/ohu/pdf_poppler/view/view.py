from PyQt5 import QtCore
from gizmo.ui.view import View

from .item import Item
from .cursor import Cursor

class PdfView(View):

    def __init__(
            self, 
            *args, 
            item_class=Item,
            cursur_class=Cursor,
            **kwargs):

        super().__init__(
                *args, 
                item_class=Item,
                cursor_class=Cursor,
                **kwargs
                )

    def prepareView(self, x=0, y=0, p=0):

        vv, hv = 0, 0
        s = self.scene()
        r = s.sceneRect()
        l, t = r.left(), r.top()
        w, h = r.width(), r.height()
        for j, i in enumerate(self.m_items):
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
            i.setResol(x, y)
            dw= i.displayedWidth()
            dh = i.displayedHeight()
            fitPageSize=[w/float(dw), h/float(dh)]
            width_ratio=w/dw
            scale = {
                'ScaleFactor': i.scale,
                'FitToWindowWidth': width_ratio,
                'FitToWindowHeight': min(fitPageSize)
                }
            s=scale[self.scaleMode]
            i.setScaleFactor(s)
        h = self.m_layout.m_mode.pageSpacing
        l, r, h = self.m_layout.load(
                items, 
                height=h
                )
        self.scene().setSceneRect(l, 0.0, r-l, h)

    def goTo(
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
            clip=self.app.qapp.clipboard()
            clip.setText(' '.join(t))
            self.select()
            self.refresh()

    def open(self, *arg, **kwargs):

        pos=kwargs.get('position', None)
        if pos:
            p=kwargs.get('page', None)
            loc=self.getLocation(pos)
            if type(loc)==tuple:
                x, y = loc
                self.goTo(p, x, y)
            elif type(loc)==list:
                topLeft=loc[0].topLeft() 
                x, y = topLeft.x(), topLeft.y()
                self.goTo(p, x, y)

    def getLocation(self, loc=None):

        if not loc:
            x, y = self.getPosition()
            x, y = str(x), str(y)
            return ':'.join([x, y])
        elif type(loc)==list:
            t=[]
            for i in loc: 
                x=str(i.x())[:6]
                y=str(i.y())[:6]
                w=str(i.width())[:6]
                h=str(i.height())[:6]
                t+=[f'{x}:{y}:{w}:{h}']
            return '_'.join(t)
        elif type(loc)==str:
            l=loc.split(':')
            f=float
            if len(l)==2:
                return f(l[0]), f(l[1])
            else:
                t=[]
                for i in loc.split('_'):
                    r=QtCore.QRectF
                    x, y, w, h = tuple(i.split(':'))
                    t+=[r(f(x), f(y), f(w), f(h))]
                return t

    def annotate(self, *args, **kwargs):

        if self.m_model:
            self.m_model.annotate(
                    *args, **kwargs)
