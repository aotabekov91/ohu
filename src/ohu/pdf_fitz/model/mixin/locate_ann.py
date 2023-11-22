from PyQt5 import QtCore
from .locate import Locate

class AnnotateLocate: 

    def delAnnotationLocator(self, data=None):

        if data:
            aid=data.get('id', None)
            elem=self.getAnnElement(data)
            elem.deannotate(data)
            return self.createLocator({'id': aid})
        return self.createLocator()

    def getAnnotationLocator(self, data=None):

        if data:
            data['hash']=self.id()
            data['kind']=self.kind()
            data['page']=self.getAnnPage(data)
            data['position']=self.getAnnLocation(data)
            data['content']=self.getAnnContent(data)
        return self.createLocator(data)

    def setAnnotationLocator(self, data=None):

        if data:
            data['box']=self.getAnnBox(data)
            elem=self.getAnnElement(data)
            elem.annotate(data)
        return self.createLocator(data)

    def openAnnotationLocator(self, data=None):

        v=data.get('view', None)
        i=data.get('item', None)
        b=data.get('box', None)
        if all([v, i, b]):
            tl=b[0].topLeft()
            v.goto(i.index(), tl.x(), tl.y())

    def getAnnBox(self, data):

        box=data.get('box', None)
        if box: return box
        t=[]
        loc=data['position']
        for i in loc.split('_'):
            f=float
            r=QtCore.QRectF
            x, y, w, h = tuple(i.split(':'))
            t+=[r(f(x), f(y), f(w), f(h))]
        return t

    def getAnnElement(self, data):

        idx=data['page']
        return self.element(idx)

    def getAnnPage(self, data):

        item=data.get('item', None)
        elem=data.get('element', None)
        if item and not elem:
            elem=item.element()
        if elem:
            return elem.index()

    def getAnnContent(self, data):

        i=data.get('item', None)
        e=data.get('element', None)
        if i and not e: e=i.element()
        if not e: return ''
        t=[]
        b=data.get('box', [])
        for i in b:
            n=e.extract(box=i, kind='text')
            t+=[n.strip('\n')]
        return ' '.join(t)

    def getAnnLocation(self, data):

        t=[]
        box=data.get('box', [])
        for i in box: 
            x=str(i.x())[:6]
            y=str(i.y())[:6]
            w=str(i.width())[:6]
            h=str(i.height())[:6]
            t+=[f'{x}:{y}:{w}:{h}']
        return '_'.join(t)
