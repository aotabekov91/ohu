from PyQt5 import QtCore, QtGui
from gizmo.widget.model import BaseElement

class ImageQtElement(
        BaseElement,
        QtCore.QObject
        ):

    def size(self):
        
        return QtCore.QSizeF(
                self.m_idata.size())

    def setup(self):

        self.m_idata=QtGui.QImage(
                self.m_data)
    
    def render(
            self, 
            hres=72, 
            vres=72, 
            rotate=0, 
            rect=None
            ):

        w, h = -1, -1
        if rect:
            w = int(rect.width())
            h = int(rect.height())
        return self.m_idata.scaled(
                w, h, QtCore.Qt.KeepAspectRatio)
