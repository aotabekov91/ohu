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
            layout=Layout,
            **kwargs,
            ):

        self.m_prev = 0
        self.m_curr = 0
        self.m_items=[]
        self.m_elements=[]
        self.delta = 0.05
        self.s_cache = {}
        self.m_paintlinks=False
        super().__init__(
                app=app, 
                layout=layout, 
                **kwargs)
        self.cursor=Cursor(self)

    def initialize(self):
        self.fitToPageWidth()

    def connect(self):

        super().connect()
        self.selection.connect(
                self.app.display.viewSelection)

    def getPosition(self):

        i=self.m_items[self.m_curr]
        r=i.boundingRect().translated(i.pos())
        tl=self.viewport().rect().topLeft()
        tl=self.mapToScene(tl)
        x=(tl.x() -r.x())/r.width()
        y=(tl.y() -r.y())/r.height()
        return x, y

    def setModel(self, model):

        super().setModel(model)
        if model:
            elems = model.elements()
            pages = elems.values()
            self.m_model = model
            self.m_elements = pages
            self.prepareItems()
            self.updateSceneAndView()
            self.initialize()

    def refresh(self):

        for i in self.getItems():
            i.refresh(dropCache=True)

    def prepareView(
            self, 
            changeLeft=0., 
            changeTop=0., 
            visiblePage=0,
            goto=False,
            ):

        r = self.scene().sceneRect()
        left = r.left()
        top = r.top()
        width = r.width()
        height = r.height()
        verticalValue = 0
        horizontalValue = 0
        if visiblePage == 0: 
            visiblePage = self.m_curr
        items=self.getItems()
        for idx, p in enumerate(items):
            brect = p.boundingRect().translated(p.pos())
            if self.s_settings.get('continuousMode', True):
                p.setVisible(True)
            else:
                if self.m_layout.leftIndex(idx) == self.m_curr:
                    p.setVisible(True)
                    top = brect.top()# -  self.s_settings.get('pageSpacing', 0.0)
                    height = brect.height()# + 2. *  self.s_settings.get('pageSpacing', 0,0)
                else:
                    p.setVisible(False)
                    p.cancelRender()
            if idx == visiblePage-1:
                horizontalValue = int(
                    brect.left()+changeLeft*brect.width())
                verticalValue = int(
                    brect.top()+changeTop*brect.height())
        #raise highlightIsOnPage
        self.setSceneRect(
                left, top, width, height)
        self.horizontalScrollBar().setValue(
                horizontalValue)
        self.verticalScrollBar().setValue(
                verticalValue)
        self.viewport().update()

    def reportPosition(self):

        x, y = self.getPosition()
        i=self.getItem()
        self.positionChanged.emit(
                self, i, x, y) 

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
                'FitToPageWidth': width_ratio,
                'FitToPageHeight': min(fitPageSize)
                }
            s=scale[self.s_settings.get('scaleMode', 'FitToPageHeight')]
            i.setScaleFactor(s)
        h = self.s_settings.get('pageSpacing', 0.0)
        # height=0
        l, r, h = self.m_layout.load(items, height=h)
        self.scene().setSceneRect(l, 0.0, r-l, h)

    def prepareItems(self):

        self.m_items = []
        for j, p in enumerate(self.m_elements):
            i = Item(p, self)
            p.setItem(i)
            self.m_items += [i]
            self.scene().addItem(i)

    def adjustScrollBarPolicy(self):

        scaleMode = self.s_settings.get(
                'scaleMode', 'FitToPageHeight')
        if scaleMode == 'ScaleFactor':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToPageWidth':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif scaleMode == 'FitToPageHeight':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
            policy = QtCore.Qt.ScrollBarAlwaysOff
            if self.s_settings.get('continuousView', True):
                policy = QtCore.Qt.ScrollBarAsNeeded

    def setVisiblePage(self):

        r=self.viewport().rect()
        x, w = int(r.width()/2-5), 10
        y, h =int(r.height()/2-5), 10
        v=QtCore.QRect(x, y, w, h)
        items=self.items(v)
        if items:
            page=items[0].page()
            pnum=page.index()
            self.setCurrentPage(pnum)

    def scaleMode(self):

        return self.s_settings.get(
                'scaleMode', 'FitToPageHeight')

    def setScaleFactor(self, scaleFactor):

        if self.s_settings.get('scaleFactor', 1.) != scaleFactor:
            if self.scaleMode() == 'ScaleFactor':
                self.s_settings['scaleFactor'] = str(scaleFactor)
                for page in self.m_items:
                    page.setScaleFactor(
                            scaleFactor)
                left, top = self.getPosition()
                self.updateSceneAndView(left=left, top=top)

    def setScaleMode(self, scaleMode):

        self.s_settings['scaleMode'] = scaleMode
        l, t = self.getPosition()
        self.adjustScrollBarPolicy()
        self.updateSceneAndView(l, t)
        self.scaleModeChanged.emit(
                scaleMode, self)

    def updateSceneAndView(
            self, 
            left=None, 
            top=None
            ):

        l, t = self.getPosition()
        top = top or t
        left = left or l 
        s=self.size()
        l=self.m_layout
        vw=l.width(s.width())
        vh=l.height(s.height())
        self.prepareScene(vw, vh)
        self.prepareView(left, top)

    def save(
            self, 
            source=None, 
            refresh=True
            ):

        if not source: 
            source=self.m_model.source()
        tFile=QtCore.QTemporaryFile()
        if tFile.open(): 
            tFile.close()
        save=self.m_model.save(
                tFile.fileName(), 
                withChanges=True)
        if save:
            name=tFile.fileName()
            with open(name, 'rb') as s:
                with open(source, 'wb') as d:
                    byte = s.read(1024*4)
                    while byte != b'':
                        d.write(byte)
                        byte = s.read(1024*4)
            return True
        
    def setCurrentPage(self, pnum):

        c, p = pnum, self.m_curr
        self.m_curr, self.m_prev=c, p
        if self.m_prev!=self.m_curr:
            self.itemChanged.emit(
                    self, self.getItem())
        self.reportPosition()

    def setPaintLinks(
            self, condition=True):

        self.m_paintlinks=condition
        for i in self.m_items:
            i.setPaintLinks(condition)
            i.refresh(dropCache=True)

    def update(self, refresh=False):

        i=self.getItem()
        i.refresh(dropCache=refresh)

    def updateAll(self, refresh=False):

        for i in self.m_items: 
            if i.isVisible():
                i.refresh(refresh)

    def cleanUp(self):

        for i in self.getItems(): 
            i.select()
            i.setSearched()

    def name(self):

        if self.m_model:
            return self.m_model.hash()
        return super().name()

    def currentPage(self): 
        return self.m_curr

    def totalPages(self): 
        return len(self.m_elements)

    def paintLinks(self): 
        return self.m_paintlinks

    def fitToPageWidth(self):
        self.setScaleMode('FitToPageWidth')

    def fitToPageHeight(self):
        self.setScaleMode('FitToPageHeight')

    def gotoFirst(self): 
        self.goto(1)

    def pageUp(self, digit=1):
        self.movePage('up', digit)

    def pageDown(self, digit=1):
        self.movePage('down', digit)

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

    def goto(
            self, 
            digit=None, 
            left=0., 
            top=0.
            ):

        x, y = self.getPosition()
        p = digit or len(self.m_elements)
        p-=1
        if p >= 0 and p <= len(self.m_elements):
            cp=self.m_layout.currentPage(p)
            c = self.m_curr != cp 
            c = any([c, abs(x-left) > 0.001])
            c = any([c, abs(y-top) > 0.001])
            if c:
                self.prepareView(
                        left, top, p, goto=True)
                self.setCurrentPage(p)
                self.setVisiblePage()
                

    def movePage(self, kind, digit=1):

        h=self.size().height()
        bar=self.verticalScrollBar()
        vh=self.m_layout.height(h)
        sh=self.scene().sceneRect().height()
        if kind=='up':
            dx=bar.value() - vh*digit
            dx=max(0, dx) 
        elif kind=='down':
            dx=bar.value() + vh*digit
            dx=min(sh, dx) 
        bar.setValue(int(dx))
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
        l, t = self.getPosition()
        for item in self.m_items: 
            n_zf=zf*item.scale()
            item.setScaleFactor(n_zf)
        self.updateSceneAndView(l, t)

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
        
    def next(self): 

        l=self.m_layout
        c=len(self.m_elements)
        cur=l.nextPage(
                self.m_curr, c)
        self.goto(cur)

    def prev(self):

        l=self.m_layout
        c=len(self.m_elements)
        cur=l.previousPage(
                self.m_curr, c)
        self.goto(cur)
        
    def getItems(self): 
        return self.m_items

    def settings(self): 
        return self.s_settings

    def getItem(self, idx=None):

        idx = idx or self.m_curr
        return self.m_items[idx]

    def readjust(self):

        l, t=self.getPosition()
        self.updateSceneAndView(l, t)
