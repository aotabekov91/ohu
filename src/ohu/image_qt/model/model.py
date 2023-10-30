import os
from gizmo.ui.view.model import Model as Base

from .element import Element

fmt = ('.BMP', 
       '.GIF', 
       '.JPG',
       '.JPEG', 
       '.PNG', 
       '.PBM', 
       '.PGM', 
       '.PPM', 
       '.TIFF', 
       '.XBM'
       )

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
        self.m_data=self.getImages(self.m_id)
        self.setElements()

    def getImages(self, folder):
        
        data = []
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if not file.upper().endswith(fmt):
                    continue
                p = os.path.join(folder, file)
                data.append(p)
        return data

    def setElements(self):

        e={}
        for i, d in enumerate(self.m_data):
            e[i+1] = Element(
                    data=d,
                    index=i+1,
                    model=self)
        self.m_elements=e
