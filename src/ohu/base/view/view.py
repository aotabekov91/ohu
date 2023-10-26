from PyQt5 import QtCore
from gizmo.ui import View as BaseView

from .item import Item
from .cursor import Cursor
from .layout import Layout

class View(BaseView):

    scaleModeChanged = QtCore.pyqtSignal(
            object, object)
    scaleFactorChanged = QtCore.pyqtSignal(
            object, object)
    continuousModeChanged = QtCore.pyqtSignal(
            bool, object)

    def __init__(
            self, 
            app=None, 
            item_class=Item,
            layout_class=Layout,
            cursor_class=Cursor,
            **kwargs,
            ):

        self.m_items=[]
        self.delta = 0.05
        self.s_cache = {}
        self.m_elements={}
        self.m_curr = None 
        self.m_prev = None 
        self.item_class=item_class
        self.cursor_class=cursor_class
        super().__init__(
                app=app, 
                layout_class=layout_class,
                **kwargs
                )
        self.cursor=self.cursor_class(self)

    def cleanUp(self):
        pass

    def count(self): 
        return len(self.m_items)
    
    def getItems(self): 
        return self.m_items

    def settings(self): 
        return self.s_settings

    def prepareView(self, *args, **kwargs):
        pass

    def prepareScene(self, *args, **kwarags):
        pass

    def initialize(self):
        self.setVisiblePage()

    def fitToWindowWidth(self):
        self.setScaleMode('FitToWindowWidth')

    def fitToWindowHeight(self):
        self.setScaleMode('FitToWindowHeight')

    def gotoFirst(self): 
        self.goto(1)

    def item(self, idx=None):

        if idx is not None:
            idx-=1
        else:
            idx=self.m_curr
        return self.m_items[idx]

    def currentItem(self):
        return self.item()

    def readjust(self):

        l, t=self.getPosition()
        self.updateView(l, t)

    def name(self):

        if self.m_model:
            return self.m_model.id()
        return super().name()
    
    def connect(self):

        super().connect()
        self.selection.connect(
                self.app.display.viewSelection)

    def setModel(self, m):

        super().setModel(m)
        if m:
            self.m_model = m
            self.setItems(m)
            self.updateView()
            self.initialize()

    def updateView(self, x=None, y=None):

        l, t = self.getPosition()
        top = y or t
        left = x or l 
        s=self.size()
        l=self.m_layout
        vw=l.width(s.width())
        vh=l.height(s.height())
        self.prepareScene(vw, vh)
        self.prepareView(left, top)

    def setItems(self, model):

        self.m_items = []
        elem=model.elements()
        for e in elem.values():
            self.setItem(e)

    def setItem(self, e):

        i = self.item_class(
                element=e, 
                view=self,
                index=e.index(),
                )
        e.setItem(i)
        self.m_items += [i]
        self.scene().addItem(i)

    def getPosition(self):

        if self.m_curr:
            i=self.m_items[self.m_curr]
            r=i.boundingRect().translated(i.pos())
            tl=self.viewport().rect().topLeft()
            tl=self.mapToScene(tl)
            x=(tl.x() -r.x())/r.width()
            y=(tl.y() -r.y())/r.height()
            return x, y
        return 0, 0


    def reportPosition(self):

        x, y = self.getPosition()
        i=self.currentItem()
        self.positionChanged.emit(
                self, i, x, y) 

    def setVisiblePage(self):

        r=self.viewport().rect()
        x, w = int(r.width()/2-5), 10
        y, h =int(r.height()/2-5), 10
        v=QtCore.QRect(x, y, w, h)
        items=self.items(v)
        if items:
            e=items[0].element()
            m_curr=e.index()-1
            self.setCurrent(m_curr)

    def setScaleFactor(self, factor):

        if self.s_settings.get('scaleFactor', 1.) != factor:
            if self.scaleMode() == 'ScaleFactor':
                self.s_settings['scaleFactor'] = str(factor)
                for i in self.m_items:
                    i.setScaleFactor(factor)
                self.updateView()

    def setScaleMode(self, mode):

        self.s_settings['scaleMode'] = mode
        self.adjustScrollBarPolicy()
        self.updateView()
        self.scaleModeChanged.emit(mode, self)

    def scaleMode(self):

        return self.s_settings.get(
                'scaleMode', 'FitToWindowHeight')

    def adjustScrollBarPolicy(self):

        scaleMode = self.s_settings.get(
                'scaleMode', 'FitToWindowHeight')
        if scaleMode == 'ScaleFactor':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToWindowWidth':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToWindowHeight':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
            policy = QtCore.Qt.ScrollBarAlwaysOff
            if self.s_settings.get('continuousView', True):
                policy = QtCore.Qt.ScrollBarAsNeeded

    def setCurrent(self, pnum):

        if self.m_curr!=pnum:
            self.m_prev=self.m_curr
            self.m_curr=pnum
            c=self.currentItem()
            self.itemChanged.emit(self, c)
        self.reportPosition()
        
    def refresh(self):

        for i in self.getItems():
            i.refresh(dropCache=True)

    def update(self, refresh=False):

        i=self.currentItem()
        i.refresh(dropCache=refresh)

    def updateAll(self, refresh=False):

        for i in self.m_items: 
            if i.isVisible():
                i.refresh(refresh)

    def prev(self):

        c=self.count()
        l=self.m_layout
        cur=l.previousPage(self.m_curr, c)
        self.goto(cur)
        
    def next(self): 

        c=self.count()
        l=self.m_layout
        cur=l.nextPage(self.m_curr, c)
        self.goto(cur)

    def setPaintLinks(self, cond=True):

        self.m_paintlinks=cond
        for i in self.m_items:
            i.setPaintLinks(cond)
            i.refresh(dropCache=True)

    def paintLinks(self): 
        return self.m_paintlinks
    
    def screenLeft(self, digit=1):
        self.moveScreen('left', digit)
        
    def screenRight(self, digit=1):
        self.moveScreen('right', digit)

    def screenUp(self, digit=1):
        self.moveScreen('up', digit)

    def screenDown(self, digit=1):
        self.moveScreen('down', digit)

    def zoomIn(self, digit=1):
        self.setZoom('in', digit)

    def zoomOut(self, digit=1): 
        self.setZoom('out', digit)
        
    def down(self, digit=1):
        self.move('down', digit)

    def up(self, digit=1):
        self.move('up', digit)

    def left(self, digit=1):
        self.move('left', digit)

    def right(self, digit=1):
        self.move('right', digit)

    def goto(self, *args, **kwargs):
        pass

    def moveScreen(self, kind, digit=1):

        h=self.size().height()
        vbar=self.verticalScrollBar()
        hbar=self.horizontalScrollBar()
        vh=self.m_layout.height(h)
        vw=self.m_layout.height(h)
        sh=self.scene().sceneRect().height()
        sw=self.scene().sceneRect().height()
        if kind=='up':
            dx=vbar.value() - vh*digit
            dx=max(0, dx) 
            vbar.setValue(int(dx))
        elif kind=='down':
            dx=vbar.value() + vh*digit
            dx=min(sh, dx) 
            vbar.setValue(int(dx))
        elif kind=='left':
            dy=hbar.value() - vw*digit
            dy=max(0, dy) 
            hbar.setValue(int(dy))
        elif kind=='right':
            dy=hbar.value() + vw*digit
            dy=min(sw, dy) 
            hbar.setValue(int(dy))
        self.setVisiblePage()

    def setZoom(self, kind='out', digit=1):

        if self.scaleMode() != 'ScaleFactor': 
            self.setScaleMode('ScaleFactor')
        zf = self.s_settings.get(
                'zoomFactor', .1)
        if kind=='out':
            zf=(1.-zf)**digit
        elif kind=='in':
            zf=(1.+zf)**digit
        x, y = self.getPosition()
        for item in self.m_items: 
            n_zf=zf*item.scale()
            item.setScaleFactor(n_zf)
        self.updateView(x, y)

    def move(self, kind, digit=1):

        s=self.size()
        l=self.m_layout
        sr=self.scene().sceneRect()
        vbar=self.verticalScrollBar()
        hbar=self.horizontalScrollBar()
        vw=l.width(s.width())
        vh=l.height(s.height())
        inc_vh=vh*self.delta
        inc_vw=vw*self.delta
        if kind=='down':
            dx=vbar.value() + inc_vh*digit
            dx=min(sr.height(), dx)
            vbar.setValue(int(dx))
        elif kind=='up':
            dx=vbar.value() - inc_vh*digit
            dx=max(0, dx)
            vbar.setValue(int(dx))
        elif kind=='right':
            dx=hbar.value() + inc_vw*digit
            hbar.setValue(int(dx))
        elif kind=='left':
            dx=hbar.value() - inc_vw*digit
            hbar.setValue(int(dx))
        self.setVisiblePage()
