from gizmo.vimo.view.mixin import XYPos as Base

class XYPos(Base):

    def getLocator(self, kind=None):
        
        loc={}
        i=self.currentItem()
        mid=self.m_model.id()
        if i:
            e=i.element()
            eid=e.index()
            k=self.m_model.kind
            l=self.getLocation()
            loc={
               'kind': k,
               'hash' : mid,
               'page' : eid,
               'position' : l,
               }
        return loc

    def setLocator(self, loc, kind=None):

        pos=loc.get('position', None)
        l=self.parseLocation(pos)
        if l: 
            i, x, y = l
            self.goto(i, x, y)
