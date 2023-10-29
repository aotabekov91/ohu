import os
import hashlib
from popplerqt5 import Poppler
from PyQt5 import QtCore, QtGui
from gizmo.ui.view.model import Model as Base

from .element import Element

class PdfModel(Base):

    def kind(self):
        return 'document'

    def assignId(self, source):

        if os.path.isfile(source):
            source=os.path.expanduser(source)
            shash = hashlib.md5()
            with open(source, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    shash.update(chunk)
                    chunk = f.read(4096)
            dhash=shash.hexdigest()
            self.setId(dhash)
        else:
            self.setId(None)

    def load(self, source):

        d, e = None, {}
        pd=Poppler.Document
        d = pd.load(source)
        if d:
            d.setRenderHint(pd.Antialiasing)
            d.setRenderHint(pd.TextAntialiasing)
            e=self.setElements(d)
        self.m_data, self.m_elements = d, e
        self.assignId(source)

    def nativeAnnotations(self):

        a=[]
        for i, p in self.m_elements.items():
            a+=p.nativeAnnotations()
        return a

    def setannotations(self):

        a=[]
        for p in self.m_elements.values():
            a+=p.annotations()
        return a

    def annotations(self):

        anns=self.setannotations()
        nats=self.nativeAnnotations()
        for a in anns:
            a['type']='set'
        for n in nats:
            data={
                  'pAnn':n,
                  'type': 'native',
                  'hash': self.id(),
                  'kind': 'document',
                  'text': n.contents(),
                  'content': n.contents(),
                  'page': n.element().index(),
                  'color': QtGui.QColor(n.color()),
                  }
            anns+=[data]
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
            e[i+1] = Element(
                    data=d, 
                    index=i+1,
                    model=self)
        return e

    def search(self, text):

        f={}
        elem=self.elements()
        for i, p in enumerate(elem):
            m=p.search(text)
            if len(m)>0: f[i]=m
        return f

    def loadOutline(self):

        t=self.m_data.toc()
        m=QtGui.QStandardItemModel()
        if t!=0:
            try:
                d=self.m_data
                c=t.firstChild()
                r=m.invisibleRootItem()
                self.getOutline(d, c, r)
            except:
                pass
        return m

    def getOutline(self, d, c, r):

        t=QtCore.Qt
        e=c.toElement()
        ldes=0
        i=QtGui.QStandardItem(e.tagName())
        i.setFlags(t.ItemIsEnabled or t.ItemIsSelectable)
        if e.hasAttribute('Destination'):
            ldes=Poppler.LinkDestination(
                    e.attribute('Destination'))
        elif e.hasAttribute('DestinationName'):
            ldes=self.m_data.linkDestination(
                    e.attribute('DestinationName'))
        if ldes!=0:
            top=0.
            left=0.
            pn=ldes.pageNumber()
            if pn<1: 
                pn=1
            if pn>d.numPages(): 
                pn=d.numPages()
            if ldes.isChangeLeft():
                left=ldes.left()
                if left<0.: left=0.
                if left>1.: left=1.
            if ldes.isChangeTop():
                top=ldes.top()
                if top<0.: top=0.
                if top>1.: top=1.
            del ldes
            i.setData(pn, QtCore.Qt.UserRole+1)
            i.setData(left, QtCore.Qt.UserRole+2)
            i.setData(top, QtCore.Qt.UserRole+3)
            i.setData(e.tagName(), QtCore.Qt.UserRole+5)
            pageItem=i.clone()
            pageItem.setText(str(pn))
            pageItem.setTextAlignment(QtCore.Qt.AlignRight)
            # if allow also pages the look of outline becomes ugly
            # parent.appendRow([item, pageItem])
            r.appendRow(i)
        siblingNode=c.nextSibling()
        if not siblingNode.isNull():
            self.getOutline(d, siblingNode, r)
        cnode=c.firstChild()
        if not cnode.isNull():
            self.getOutline(d, cnode, i)

    def annotate(self, idx=None, **kwargs):

        e=self.element(idx)
        if e: e.annotate(**kwargs)
