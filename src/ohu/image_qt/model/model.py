import os
from gizmo.ui.view.model import Model as Base

from .element import Element

class ImageQtModel(Base):

    f='|'.join([
      'png', 
      'bmp', 
      'gif', 
      'x[bp]m',
      'p[bgp]m', 
      'jp(e){0,1}g', 
      ])
    pattern=f'.*({f})$'

    def kind(self):
        return 'image'

    def assignId(self, source):

        if os.path.exists(source):
            dname=os.path.dirname(source)
            self.setId(dname)
        else:
            self.setId(None)

    def load(self, source):

        self.assignId(source)
        self.m_data=self.getFiles(self.m_id)
        self.setElements()

    def getFiles(self, dir):
        
        d = []
        if os.path.isdir(dir):
            for f in os.listdir(dir):
                if self.isCompatible(f):
                    p = os.path.join(dir, f)
                    d.append(p)
        return d

    def setElements(self):

        e={}
        for i, d in enumerate(self.m_data):
            e[i+1] = Element(
                    data=d,
                    index=i+1,
                    model=self)
        self.m_elements=e
