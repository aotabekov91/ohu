from PyQt5 import QtCore
from .locate import Locate

class AnnotateLocate: 

    def delAnnotationLocator(self, data={}):

        if data:
            idx=data.get('id', None)
            e=self.getAnnElement(data)
            e.deannotate(data)
            return self.createLocator({'id': idx})
        return self.createLocator(data)

    def getAnnotationLocator(self, data={}):

        if data:
            data['hash']=self.id()
            data['kind']=self.kind
            data['position']=self.getAnnLocation(data)
            data['content']=self.getAnnContent(data)
            data['text']=data['content']
        return self.createLocator(data)

    def setAnnotationLocator(self, data={}):

        if data:
            p, b=self.getAnnBox(data)
            data['page'], data['box']=p, b
            e=self.getAnnElement(data)
            e.annotate(data)
        return self.createLocator(data)

    def openAnnotationLocator(self, data={}):

        b=data.get('box', None)
        p=data.get('page', None)
        v=data.get('view', None)
        if all([v, i, b]):
            tl=b[0].topLeft()
            v.goto(p, tl.x(), tl.y())

    def getAnnBox(self, data={}):

        b=data.get('box', None)
        if b: return b
        t=[]
        ploc=data['position']
        s=ploc.split('|', 1)
        p, loc = int(s[0]), s[1]
        for i in loc.split('_'):
            f=float
            r=QtCore.QRectF
            x, y, w, h = tuple(i.split(':'))
            t+=[r(f(x), f(y), f(w), f(h))]
        return p, t

    def getAnnElement(self, data={}):

        idx=data['page']
        return self.element(idx)

    def getAnnPage(self, data={}):

        i=data.get('item', None)
        e=data.get('element', None)
        if i and not e: e=i.element()
        if e: return e.index()

    def getAnnContent(self, data={}):

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

    def getAnnLocation(self, data={}):

        t=[]
        p=self.getAnnPage(data)
        b=data.get('box', [])
        for i in b: 
            x=str(i.x())[:6]
            y=str(i.y())[:6]
            w=str(i.width())[:6]
            h=str(i.height())[:6]
            t+=[f'{x}:{y}:{w}:{h}']
        loc='_'.join(t)
        return f'{p}|{loc}'
