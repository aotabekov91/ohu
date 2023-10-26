from popplerqt5 import Poppler
from PyQt5 import QtCore, QtGui
from ohu.base.model import Model as Base

from .element import Element

class Model(Base):

    def load(self, source):

        d, e = None, {}
        pd=Poppler.Document
        d = pd.load(source)
        if d:
            d.setRenderHint(pd.Antialiasing)
            d.setRenderHint(pd.TextAntialiasing)
            e=self.setElements(d)
        self.m_data, self.m_elements = d, e

    def nativeAnnotations(self):

        anns=[]
        for i, p in self.m_elements.items():
            anns+=p.nativeAnnotations()
        return anns

    def annotations(self):

        anns=[]
        for i, p in self.m_elements.items():
            anns+=p.annotations()
        return anns

    def save(self, source, withChanges):

        pconf=self.m_data.pdfConverter()
        pconf.setOutputFileName(source)
        if withChanges:
            c1 = pconf.pdfOptions()
            c2 = Poppler.PDFConverter.WithChanges
            pconf.setPDFOptions(c1 or c2)
        return pconf.convert()

    def setElements(self, data):

        e={}
        for i in range(data.numPages()):
            d=data.page(i)
            e[i] = Element(
                    data=d, 
                    index=i, 
                    model=self
                    )
        return e

    def search(self, text):

        f={}
        for i, p in enumerate(self.elements()):
            m=p.search(text)
            if len(m)>0: f[i]=m
        return f

    def loadOutline(self):

        t=self.m_data.toc()
        m=QtGui.QStandardItemModel()
        if t!=0:
            try:
                self.getOutline(
                        self.m_data,
                        t.firstChild(),
                        m.invisibleRootItem()
                        )
            except:
                pass
        return m

    def getOutline(self, data, child, root):

        linkDestination=0
        element=child.toElement()
        item=QtGui.QStandardItem(element.tagName())
        item.setFlags(
                QtCore.Qt.ItemIsEnabled or QtCore.Qt.ItemIsSelectable)
        if element.hasAttribute('Destination'):
            linkDestination=Poppler.LinkDestination(
                    element.attribute('Destination'))
        elif element.hasAttribute('DestinationName'):
            linkDestination=self.m_data.linkDestination(
                    element.attribute('DestinationName'))
        if linkDestination!=0:
            top=0.
            left=0.
            page=linkDestination.pageNumber()
            if page<1: 
                page=1
            if page>data.numPages(): 
                page=data.numPages()
            if linkDestination.isChangeLeft():
                left=linkDestination.left()
                if left<0.: left=0.
                if left>1.: left=1.
            if linkDestination.isChangeTop():
                top=linkDestination.top()
                if top<0.: top=0.
                if top>1.: top=1.
            del linkDestination
            item.setData(page, QtCore.Qt.UserRole+1)
            item.setData(left, QtCore.Qt.UserRole+2)
            item.setData(top, QtCore.Qt.UserRole+3)
            item.setData(element.tagName(), QtCore.Qt.UserRole+5)
            pageItem=item.clone()
            pageItem.setText(str(page))
            pageItem.setTextAlignment(QtCore.Qt.AlignRight)
            # if allow also pages the look of outline becomes ugly
            # parent.appendRow([item, pageItem])
            root.appendRow(item)
        siblingNode=child.nextSibling()
        if not siblingNode.isNull():
            self.getOutline(data, siblingNode, root)
        childNode=child.firstChild()
        if not childNode.isNull():
            self.getOutline(data, childNode, item)

    def getPosition(self, bounds):

        t=[]
        for b in bounds: 
            x=str(b.x())[:6]
            y=str(b.y())[:6]
            w=str(b.width())[:6]
            h=str(b.height())[:6]
            t+=[f'{x}:{y}:{w}:{h}']
        return '_'.join(t)

    def getBoundaries(self, pos):

        a=[]
        for t in pos.split('_'):
            x, y, w, h = tuple(t.split(':'))
            a+=[QtCore.QRectF(
                float(x), 
                float(y), 
                float(w), 
                float(h))]
        return a
