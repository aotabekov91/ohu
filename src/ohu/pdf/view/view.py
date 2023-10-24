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
            self, app, layout=Layout):

        super().__init__(app, layout)
        self.m_prev = 1 
        self.m_curr = 1 
        self.m_items=[]
        self.s_cache = {}
        self.m_paintlinks=False
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

    def getPosition(self, left=0., top=0.):

        p=self.m_items[self.m_curr-1]
        r=p.boundingRect().translated(p.pos())
        topLeft=self.mapToScene(
                self.viewport().rect().topLeft())
        left=(topLeft.x() -r.x())/r.width()
        top=(topLeft.y() -r.y())/r.height()
        return left, top

    def next(self): 

        self.goto(self.m_layout.nextPage(
            self.m_curr, len(self.m_pages)))

    def prev(self):

        self.goto(self.m_layout.previousPage(
            self.m_curr, len(self.m_pages)))

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
            visiblePage=0):

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

        self.setSceneRect(left, top, width, height)
        self.horizontalScrollBar().setValue(horizontalValue)
        self.verticalScrollBar().setValue(verticalValue)
        self.viewport().update()

    def reportPosition(self):

        left, top = self.getPosition()
        self.positionChanged.emit(
                self, 
                self.pageItem(), 
                left, 
                top)

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
            pageItem = Item(page, self)
            page.setPageItem(pageItem)
            self.m_items += [pageItem]
            self.scene().addItem(pageItem)

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

    def down(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())*.05
        dx=self.verticalScrollBar().value() + visibleHeight
        h=int(self.scene().sceneRect().height())
        self.verticalScrollBar().setValue(h)
        if dx<=self.scene().sceneRect().height():
            self.verticalScrollBar().setValue(int(dx-0.5))
        self.setFromVisible()

    def up(self):

        visibleHeight=self.m_layout.visibleHeight(
                self.size().height())*.05
        dx=self.verticalScrollBar().value() - visibleHeight
        self.verticalScrollBar().setValue(0)
        if dx>=0:
            self.verticalScrollBar().setValue(int(dx+0.5))
        self.setFromVisible()
        
    def left(self):

        self.horizontalScrollBar().setValue(
                int(self.horizontalScrollBar().value()*1.1))
        self.setFromVisible()

    def right(self):

        self.horizontalScrollBar().setValue(
                int(self.horizontalScrollBar().value()*0.9))
        self.setFromVisible()

    def pageUp(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())
        dx=self.verticalScrollBar().value() - visibleHeight
        if dx>=0:
            self.verticalScrollBar().setValue(int(dx+5))
        else:
            self.verticalScrollBar().setValue(0)
        self.setFromVisible()

    def pageDown(self):

        visibleHeight=self.m_layout.visibleHeight(self.size().height())
        dx=self.verticalScrollBar().value() + visibleHeight
        if dx<=self.scene().sceneRect().height():
            self.verticalScrollBar().setValue(int(dx-5))
        else:
            self.verticalScrollBar().setValue(int(self.scene().sceneRect().height()))
        self.setFromVisible()

    def setFromVisible(self):

        r=self.viewport().rect()
        v=QtCore.QRect(
                int(r.width()/2)-5, int(r.height()/2-5), 10, 10)
        items=self.items(v)
        if items:
            self.setCurrentPage(
                    items[0].page().pageNumber())
        self.reportPosition()

    def scaleMode(self):

        return self.s_settings.get(
                'scaleMode', 'FitToPageHeight')

    def zoomIn(self, digit=1):

        for i in range(digit):
            self._zoom(kind='in')

    def zoomOut(self, digit=1): 

        for i in range(digit):
            self._zoom(kind='out')

    def _zoom(self, kind='out'):

        zoomFactor = self.s_settings.get('zoomFactor', .1)
        if self.scaleMode() != 'ScaleFactor': 
            self.setScaleMode('ScaleFactor')
        if kind=='out':
            zoomFactor=1.-zoomFactor
        elif kind=='in':
            zoomFactor=1.+zoomFactor
        l, p = self.getPosition()
        for item in self.m_items: 
            item.setScaleFactor(
                    zoomFactor*item.scale())
        self.updateSceneAndView(left=l, top=p)

    def setScaleFactor(self, scaleFactor):

        if self.s_settings.get('scaleFactor', 1.) != scaleFactor:
            if self.scaleMode() == 'ScaleFactor':
                self.s_settings['scaleFactor'] = str(scaleFactor)
                for page in self.m_items:
                    page.setScaleFactor(
                            scaleFactor)
                left, top = self.getPosition()
                self.updateSceneAndView(left=left, top=top)

    def fitToPageWidth(self):
        self.setScaleMode('FitToPageWidth')

    def fitToPageHeight(self):
        self.setScaleMode('FitToPageHeight')

    def setScaleMode(self, scaleMode):

        self.s_settings['scaleMode'] = scaleMode
        left, top = self.getPosition()
        self.getPosition(left, top)
        self.adjustScrollBarPolicy()
        self.updateSceneAndView()
        self.scaleModeChanged.emit(scaleMode, self)

    def updateSceneAndView(
            self, 
            left=None, 
            top=None):

        if not left or not top:
            left, top = self.getPosition()
        visibleWidth=self.m_layout.visibleWidth(
                self.size().width())
        visibleHeight=self.m_layout.visibleHeight(
                self.size().height())
        self.prepareScene(
                visibleWidth, visibleHeight)
        self.prepareView(
                left, top)

    def save(self, path=False, refresh=True):

        if path is False: 
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
            item=self.pageItem()
            self.itemChanged.emit(
                    self, item)

    def setPaintLinks(self, condition=True):

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

    def gotoEnd(self): 
        self.goto(len(self.m_pages))

    def gotoBegin(self): 
        self.goto(1)

    def currentPage(self): 
        return self.m_curr

    def totalPages(self): 
        return len(self.m_pages)

    def paintLinks(self): 
        return self.m_paintlinks

    def goto(
            self, 
            page=1, 
            left=0., 
            top=0.
            ):

        if page >= 0 and page <= len(self.m_pages):
            l, t = self.getPosition()
            cpage=self.m_layout.currentPage(page)
            c = self.m_curr != cpage 
            c = any([c, abs(l-left) > 0.001])
            c = any([c, abs(t-top) > 0.001])
            if c:
                self.prepareView(left, top, page)
                self.setFromVisible()
