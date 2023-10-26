from PyQt5 import QtCore
from ohu.base.model import Annotation as Base

class Annotation(Base):

    def __init__(self, data):

        super().__init__(data)
        self.m_aData={'data': data}

    def id(self): 
        return self.m_aData.get('id', None)

    def contents(self): 
        return self.m_data.contents()

    def type(self): 
        return self.m_aData['data'].subType()

    def data(self): 
        return self.m_aData['data']

    def aData(self): 
        return self.m_aData

    def setAData(self, data): 
        self.m_aData=data

    def boundary(self): 
        return self.m_aData['data'].boundary()

    def setId(self, idx): 

        super().setId(idx)
        self.m_aData['id']=idx

    def setColor(self, color):

        style=self.m_aData['data'].style()
        style.setColor(color)
        self.m_data.setStyle(style)

    def color(self): 

        style=self.m_aData['data'].style()
        return style.color().name()

    def position(self):

        d=self.m_data
        q=d.highlightQuads()
        tl=q[0].points[0]
        br=q[0].points[2]
        tx, ty =tl.x(), tl.y()
        bx, by = br.x(), br.y()
        p=[]
        for f in [tx, ty, bx, by]:
            p+=[str(round(f, 5))]
        fl=':'.join(p)
        tl=q[-1].points[0]
        br=q[-1].points[2]
        tx, ty = tl.x(), tl.y()
        bx, by = br.x(), br.y()
        p=[]
        for f in [tx, ty, bx, by]:
            p+=[str(round(f, 5))]
        ll=':'.join(p)
        return f'{fl}_{ll}'

    def contains(self, point):

        q=self.m_data.highlightQuads()
        for i in q: 
            p=i.points
            r=QtCore.QRectF()
            r.setTopLeft(p[0])
            r.setTopRight(p[1])
            r.setBottomRight(p[2])
            r.setBottomLeft(p[3])
            if r.contains(point): 
                return True
        return False
