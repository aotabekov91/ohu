import fitz
from PyQt5 import QtCore, QtGui
from gizmo.vimo.element import Element

class FitzElement(
        Element, 
        QtCore.QObject
        ):

    def search(self, text):
        return self.m_data.search_for(text)

    def size(self): 

        b=self.m_data.bound()
        w, h = b.width, b.height
        return QtCore.QSizeF(w, h)

    def render(
            self, 
            hres=72, 
            vres=72, 
            rotate=0, 
            rect=None
            ):

        fmt = QtGui.QImage.Format_RGB888
        x, y = int(hres/72.), int(vres/72.)
        if rect:
            s=rect.size()
            ow=self.size()
            x=s.width()/ow.width()
            y=s.height()/ow.height()
        m=fitz.Matrix(x, y)
        p=self.m_data.get_pixmap(
                matrix=m, alpha=False)
        return QtGui.QImage(
            p.samples,
            p.width,
            p.height,
            p.stride,
            fmt)
