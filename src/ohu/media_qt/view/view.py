from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from gizmo.widget.view import DirMixin, ItemMixin, BaseView

class MediaQtView(
        DirMixin,
        ItemMixin,
        BaseView,
        QtWidgets.QGraphicsView
        ):

    position='display'

    def setup(self):

        super().setup()
        self.setupPlayer()

    def setupPlayer(self):

        p = QMediaPlayer()
        o = QGraphicsVideoItem()
        s = self.contentsRect().size()
        o.setSize(QtCore.QSizeF(s))
        self.m_scene.addItem(o)
        p.setVideoOutput(o)
        self.player = p
        self.output = o

    def setModel(self, model):

        if model:
            self.m_model = model
            self.setItems()
            self.updateView()
            self.jumpToSource()

    def prepareScene(self):

        self.fitInView(
                self.output, 
                QtCore.Qt.KeepAspectRatio)

    def goTo(
            self, 
            digit=None, 
            x=0, 
            ):

        c = self.count() 
        p = digit or c 
        if 0 < p <= c:
            if self.m_curr != p:
                i=self.m_items[p]
                c=i.element().render()
                self.player.setMedia(c)
                self.player.play()
                self.setCurrentIndex(p)
