import fitz
from PyQt5 import QtCore, QtGui
from gizmo.vimo.element import Element

from .mixin import Search, Block, Links, Annotate

class FitzElement(
        Search,
        Block,
        Links,
        Element, 
        Annotate,
        QtCore.QObject):

    def setup(self):

        super().setup()
        self.setSize()
        self.matrix=fitz.Matrix(1, 1)
        self.fmt = QtGui.QImage.Format_RGB888

    def setSize(self):

        b=self.m_data.bound()
        w, h = b.width, b.height
        self.m_size=QtCore.QSizeF(w, h)

    def size(self): 
        return self.m_size

    def render(
            self, 
            hres=72, 
            vres=72, 
            rotate=0, 
            rect=None
            ):

        m=self.matrix
        if rect:
            rs=rect.size()
            os=self.size()
            x=rs.width()/os.width()
            y=rs.height()/os.height()
            m=fitz.Matrix(x, y)
        p=self.m_data.get_pixmap(
                matrix=m, alpha=False)
        return QtGui.QImage(
            p.samples,
            p.width,
            p.height,
            p.stride,
            self.fmt)
