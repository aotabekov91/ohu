from PyQt5 import QtCore, QtGui
from gizmo.ui.view.model import Element as Base

class Element(Base):

    def size(self):
        s=self.m_data.size()
        return QtCore.QSizeF(s.width(), s.height())

    def setup(self):

        super().setup()
        self.m_data=QtGui.QImage(self.m_data)
        self.setTransformers()
    
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

        x, y, w, h = (-1,)*4
        if rect:
            x = int(rect.x())
            y = int(rect.y())
            w = int(rect.width())
            h = int(rect.height())
        return self.m_data.scaled(
                w, h, QtCore.Qt.KeepAspectRatio)
