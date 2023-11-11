from PyQt5 import QtCore
from fitz import Quad, Point
from gizmo.vimo.element import mixin

class Annotate(mixin.Annotate):

    def deannotate(self, d):

        b=d['box'][0]
        b=self.m_norm.mapRect(b)
        for a in self.m_data.annots():
            p1=QtCore.QPointF(a.rect.x0, a.rect.y0)
            p2=QtCore.QPointF(a.rect.x1, a.rect.y1)
            r=QtCore.QRectF(p1, p2)
            if r.intersects(b):
                self.m_data.delete_annot(a)
                self.annotationRemoved.emit(d)
                self.changed.emit()
                return a

    def annotate(self, d):

        akind=d.get('akind', None)
        if akind=='highlight':
            p=self.m_data
            q=self.getAnnQuads(d)
            a=p.add_highlight_annot(q)
        c=d.get('color', None)
        if c: 
            s=(c.redF(), c.greenF(), c.blueF())
            a.set_colors(stroke=s)
        a.update()
        self.annotationAdded.emit(d)
        self.changed.emit()

    def getAnnQuads(self, d):

        q=[]
        r=d.get('box')
        if type(r)!=list: r=[r]
        for i in r:
            i=self.m_norm.mapRect(i)
            x, y = i.x(), i.y()
            w, h = i.width(), i.height()
            ul, ur=(x, y), (x+w, y)
            ll, lr=(x, y+h), (x+w, y+h)
            q+=[Quad(ul, ur, ll, lr)]
        return q
