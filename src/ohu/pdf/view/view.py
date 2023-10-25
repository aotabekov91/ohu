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

        self.m_prev = 1 
        self.m_curr = 1 
        self.m_items=[]
        self.m_pages=[]
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

    def readjust(self):

        l, t=self.getPosition()
        self.updateSceneAndView(l, t)

    def getPosition(self):

        p=self.m_items[self.m_curr-1]
        r=p.boundingRect().translated(p.pos())
        topLeft=self.mapToScene(
                self.viewport().rect().topLeft())
        left=(topLeft.x() -r.x())/r.width()
        top=(topLeft.y() -r.y())/r.height()
        return left, top

    def setModel(self, model):

        super().setModel(model)
        if model:
            pages = model.pages().values()
            self.m_pages = pages
            self.m_model = model
            self.preparePages()
            self.updateSceneAndView()
            self.initialize()

    def refresh(self):

        for i in self.m_items:
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
        for idx, p in enumerate(self.m_items):
            brect = p.boundingRect().translated(p.pos())
            if self.s_settings.get('continuousMode', True):
                p.setVisible(True)
            else:
                if self.m_layout.leftIndex(idx) == self.m_curr-1:
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

        l, t = self.getPosition()
        item=self.pageItem()
        self.positionChanged.emit(
                self, item, l, t) 

    def prepareScene(self, w, h):

        for item in self.m_items:
            item.setResolution(
                    self.logicalDpiX(), 
                    self.logicalDpiY())
            dw= item.displayedWidth()
            dh = item.displayedHeight()
            fitPageSize=[w/float(dw), h/float(dh)]
            width_ratio=w/dw
            scale = {
                'ScaleFactor': item.scale(),
                'FitToPageWidth': width_ratio,
                'FitToPageHeight': min(fitPageSize)
                }
            s=scale[self.s_settings.get('scaleMode', 'FitToPageHeight')]
            item.setScaleFactor(s)
        height = self.s_settings.get('pageSpacing', 0.0)
        # height=0
        left, right, height = self.m_layout.prepareLayout(
            self.m_items, height=height)
        self.scene().setSceneRect(left, 0.0, right-left, height)

    def pageItems(self): 
        return self.m_items

    def settings(self): 
        return self.s_settings

    def pageItem(self, index=None):

        if index is None: 
            index=self.m_curr-1
        return self.m_items[index]

    def preparePages(self):

        self.m_items = []
        for i, page in enumerate(self.m_pages):
            item = Item(page, self)
            page.setPageItem(item)
            self.m_items += [item]
            self.scene().addItem(item)

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
            pnum=page.pageNumber()
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
        vw=l.visibleWidth(s.width())
        vh=l.visibleHeight(s.height())
        self.prepareScene(vw, vh)
        self.prepareView(left, top)

    def save(
            self, 
            path=None, 
            refresh=True
            ):

        if not path: 
            path=self.m_model.filePath()
        tFile=QtCore.QTemporaryFile()
        if tFile.open(): 
            tFile.close()
        save=self.m_model.save(
                tFile.fileName(), 
                withChanges=True)
        if save:
            name=tFile.fileName()
            with open(name, 'rb') as s:
                with open(path, 'wb') as d:
                    byte = s.read(1024*4)
                    while byte != b'':
                        d.write(byte)
                        byte = s.read(1024*4)
            return True
        
    def setCurrentPage(self, pnum):

        self.m_prev=self.m_curr
        self.m_curr=pnum
        if self.m_prev!=self.m_curr:
            i=self.pageItem()
            self.itemChanged.emit(
                    self, i) 
        self.reportPosition()

    def setPaintLinks(
            self, condition=True):

        self.m_paintlinks=condition
        for item in self.m_items:
            item.setPaintLinks(condition)
            item.refresh(dropCache=True)

    def update(self, refresh=False):

        item=self.m_items[self.m_curr-1]
        item.refresh(dropCache=refresh)

    def updateAll(self, refresh=False):

        for item in self.m_items: 
            if item.isVisible():
                item.refresh(refresh)

    def cleanUp(self):

        for item in self.pageItems(): 
            item.select()
            item.setSearched()

    def name(self):

        if self.m_model:
            return self.m_model.hash()
        return super().name()

    def currentPage(self): 
        return self.m_curr

    def totalPages(self): 
        return len(self.m_pages)

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
            page=None, 
            left=0., 
            top=0.
            ):

        l, t = self.getPosition()
        page = page or len(self.m_pages)
        if page >= 0 and page <= len(self.m_pages):
            cpage=self.m_layout.currentPage(page)
            c = self.m_curr != cpage 
            c = any([c, abs(l-left) > 0.001])
            c = any([c, abs(t-top) > 0.001])
            if c:
                self.prepareView(
                        left, top, page, goto=True)
                self.setCurrentPage(page)
                self.setVisiblePage()
                

    def movePage(self, kind, digit=1):

        h=self.size().height()
        bar=self.verticalScrollBar()
        vh=self.m_layout.visibleHeight(h)
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
        vw=l.visibleHeight(s.width())
        vh=l.visibleHeight(s.height())
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

        self.goto(self.m_layout.nextPage(
            self.m_curr, len(self.m_pages)))

    def prev(self):

        self.goto(self.m_layout.previousPage(
            self.m_curr, len(self.m_pages)))
