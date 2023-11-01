from PyQt5 import QtCore, QtMultimedia
from gizmo.widget.model import BaseElement

class MediaQtElement(BaseElement):

    def size(self):

        return QtCore.QSizeF(
                self.m_data.size())

    def setup(self):

        self.m_url=QtCore.QUrl.fromLocalFile(
                self.m_data)
    
    def render(self):
        return QtMultimedia.QMediaContent(self.m_url)
