from PyQt5 import QtCore
from gizmo.vimo.model import mixin

class Annotate(mixin.Annotate, mixin.Locate): 

    def getLocator(self, data=None, kind=None):

        if data and kind == 'annotation':
            data['hash']=self.id()
            data['kind']=self.kind
            data['page']=self.getAnnPage(data)
            data['position']=self.getAnnLoc(data)
            data['content']=self.getAnnContent(data)
            return data
        else:
            return super().getLocator(data, kind)

    def setLocator(self, data=None, kind=None):
        raise

    def setAnnLoc(self, d):

        t=[]
        loc=d['position']
        for i in loc.split('_'):
            f=float
            r=QtCore.QRectF
            x, y, w, h = tuple(i.split(':'))
            t+=[r(f(x), f(y), f(w), f(h))]
        d['box']=t

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

    def getAnnLoc(self, data):

        t=[]
        box=data.get('box', [])
        for i in box: 
            x=str(i.x())[:6]
            y=str(i.y())[:6]
            w=str(i.width())[:6]
            h=str(i.height())[:6]
            t+=[f'{x}:{y}:{w}:{h}']
        return '_'.join(t)
