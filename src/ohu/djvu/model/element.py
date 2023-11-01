from djvu import decode
from PyQt5 import QtCore, QtGui
from gizmo.widget.model import BaseElement

class Element(
        BaseElement,
        QtCore.QObject,
        ):

    def size(self): 

        s=self.m_data.size
        return QtCore.QSizeF(*s)

    def setup(self):

        self.m_data=self.m_data.decode(wait=True)
        super().setup()

    def render(
            self, 
            hres=72, 
            vres=72, 
            rotate=0, 
            rect=None
            ):

        w, h = (-1,)*2
        if rect:
            w = int(rect.width())
            h = int(rect.height())

        pf = decode.PixelFormatRgbMask(
            0xFF0000, 0xFF00, 0xFF, bpp=32)
        pf.y_top_to_bottom = 0
        pf.rows_top_to_bottom = 1
        jb = self.m_data
        w, h = jb.size
        r = (0, 0, w, h)
        o = jb.render(0, r, r, pf)

        imgf = QtGui.QImage.Format_RGB32
        img = QtGui.QImage(o, w, h, imgf)
        img = img.convertToFormat(
            QtGui.QImage.Format_ARGB32_Premultiplied)
        return img.scaled(
                w, h, QtCore.Qt.KeepAspectRatio)
