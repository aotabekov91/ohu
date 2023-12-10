from PyQt5 import QtCore 
from gizmo.vimo import item, view

from .utils import Viewport

class Items(view.mixin.Scene):

    hasItems=True
    item_class=item.Item
    indexChanged=QtCore.pyqtSignal(object)

    def setup(self):

        self.m_curr=1
        self.m_prev=None
        self.m_viewport=Viewport()
        self.setViewport(self.m_viewport)
        self.m_viewport.updated.connect(
                self.updateItem)
        super().setup()

    def setModel(self, model):

        self.clearScene()
        if id(self.m_model)!=id(model):
            self.m_items={}
            self.m_fetched=0
            self.modelIsToBeChanged.emit(
                    self, self.m_model)
            self.m_model=model
            self.kind=model.kind
            self.setItems(model)
            self.modelLoaded.emit(
                    self, self.m_model)
            self.modelChanged.emit(
                    self.m_model)

    def updateItem(self):

        if self.m_fetched>=self.count():
            self.m_viewport.updated.disconnect(
                    self.updateItem)
        else:
            r=self.m_viewport.rect()
            r=self.mapToScene(r)
            itms=self.itemsNear(r.boundingRect())
            for i in itms:
                self.wantItem(i)
            self.redrawScene()

    def wantItem(self, i):

        if not i.scene():
            i.setVisible(True)
            self.m_fetched+=1
            self.m_scene.addItem(i)

    def setItems(self, model):

        x=self.logicalDpiX()
        y=self.logicalDpiY()
        elems=model.elements().values()
        for j, e in enumerate(elems): 
            i=self.createItem(j, e)
            i.setVisible(False)
            i.setResol(x, y)
            self.m_items[e.index()]=i
        self.redrawScene()

    def createItem(self, idx, e):

        return self.item_class(
                element=e,
                index=idx+1,
                scaleFactor=self.scaleFactor,
                config=self.m_config.get('Item', {}),
                )

    def setCurrentIndex(self, idx):

        if self.m_curr!=idx:
            c, p = idx, self.m_curr
            self.m_curr, self.m_prev=c, p
        self.indexChanged.emit(self.m_curr)

    def refresh(self):

        for j, i in self.getItems():
            i.refresh(dropCache=True)

    def updateCurrent(self, refresh=False):

        i=self.currentItem()
        i.refresh(dropCache=refresh)

    def updateVisibile(self, refresh=False):

        for i in self.m_items.values(): 
            if i.isVisible():
                i.refresh(refresh)

    def visibleItems(self): 

        r=self.viewport().rect()
        return self.items(r)

    def setVisibleItem(self):

        v=self.viewport()
        v.update()
        r=self.viewport().rect()
        x, w = int(r.width()/2-5), 10
        y, h = int(r.height()/2-5), 10
        v=QtCore.QRect(x, y, w, h)
        i=self.items(v)
        idx=self.m_curr
        if i: idx=i[0].index()
        self.setCurrentIndex(idx)

    def item(self, idx=None, element=None):

        if element:
            for i in self.m_items.values():
                if i.element()==element:
                    return i
        else:
            return self.m_items.get(idx, None)

    def count(self):

        if self.m_model:
            return self.m_model.count()
        return len(self.m_items) 

    def getItems(self):
        return self.m_items.items()

    def currentItem(self):
        return self.item(self.m_curr)

    def currentIndex(self):
        return self.m_curr

    def itemsNear(self, rect):

        for i in self.m_items.values():
            if rect.intersects(i.m_rect):
                idx=i.index()
                yield i
                h=i.m_rect.y()+i.m_rect.height()
                rh=rect.y()+rect.height()
                if h>rh: 
                    idx+=1
                    n=self.m_items.get(idx)
                    if n: yield n
                    break
