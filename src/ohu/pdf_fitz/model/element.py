import fitz
from PyQt5 import QtCore, QtGui
from gizmo.widget.model import BaseElement

class Element(BaseElement, QtCore.QObject):

    def textList(self): 
        return []

    def nativeAnnotations(self): 
        return []

    def size(self): 

        b=self.m_data.bound()
        w, h = b.width, b.height
        return QtCore.QSizeF(w, h)

    def find(self, rect, unified=False): 
        pass

    def search(self, string): 
        pass

    def setup(self):

        super().setup()
        self.m_annotations=[]
        self.setTransformers()

    def annotations(self):
        pass

    def setAnnotations(self, annotations=[]):
        pass

    def setTransformers(self):

        s=self.size()
        w, h = s.width(), s.height()
        self.m_norm=QtGui.QTransform()
        self.m_norm.reset()
        self.m_norm.scale(w, h)

    def render(
            self, 
            hres=72, 
            vres=72, 
            rotate=0, 
            rect=None
            ):

        fmt = QtGui.QImage.Format_RGB888
        x, y = int(hres/72.), int(vres/72.)
        m=fitz.Matrix(x, y)
        p=self.m_data.get_pixmap(
                matrix=m, alpha=False)
        return QtGui.QImage(
            p.samples,
            p.width,
            p.height,
            p.stride,
            fmt)

    def annotate(self, **aData):
        pass

    def addHighlightAnnotation(self, boundary, color):
        pass

    def addTextAnnotation(self, boundary, color):
        pass

    def removeAnnotation(self, aData):
        pass

    def getNativeAnnotations(self):
        pass

    def links(self):
        pass

    def getRows(self, start, end):
        pass

    def getRow(self, point):
        pass
