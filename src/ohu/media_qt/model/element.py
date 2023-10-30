from PyQt5 import QtCore, QtGui, QtMultimedia
from gizmo.ui.view.model import Element as Base

class Element(Base):

    def size(self):

        return QtCore.QSizeF(
                self.m_data.size())

    def setup(self):

        super().setup()
        self.m_url=QtCore.QUrl.fromLocalFile(
                self.m_data)
    
    def render(self):
        return QtMultimedia.QMediaContent(self.m_url)
