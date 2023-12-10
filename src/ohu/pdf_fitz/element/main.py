import fitz
from PyQt5 import QtCore, QtGui
from gizmo.vimo import element

from . import mixin

class FitzElement(
        mixin.Search,
        mixin.Block,
        mixin.Links,
        mixin.Annotate,
        element.mixin.Cache,
        element.Element, 
        QtCore.QObject
        ):

    def setup(self):

        super().setup()
        self.setSize()
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

        x, y = 1, 1
        if rect:
            rs=rect.size()
            os=self.size()
            x=rs.width()/os.width()
            y=rs.height()/os.height()
            x=round(x, 5)
            y=round(y, 5)
        p=self.m_data.get_pixmap(
                alpha=False,
                matrix=fitz.Matrix(x, y),
                )
        return QtGui.QImage(
            p.samples,
            p.width,
            p.height,
            p.stride,
            self.fmt)
