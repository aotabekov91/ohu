from gizmo.ui.view import View
from PyQt5 import QtCore, QtMultimedia, QtMultimediaWidgets

from .item import Item
from .cursor import Cursor

class MediaQtView(View):

    def __init__(
            self, 
            *args, 
            item_class=Item,
            cursur_class=Cursor,
            **kwargs):

        super().__init__(
                *args, 
                item_class=Item,
                cursor_class=Cursor,
                **kwargs
                )

    def setup(self, *args, **kwargs):

        super().setup(*args, **kwargs)
        self.player = QtMultimedia.QMediaPlayer()

    def setItems(self, model):

        self.output = QtMultimediaWidgets.QGraphicsVideoItem()
        self.scene().addItem(self.output)
        w_f = float(self.contentsRect().size().width())
        h_f = float(self.contentsRect().size().height())
        self.output.setSize(QtCore.QSizeF(w_f, h_f))
        self.player.setVideoOutput(self.output)

    def prepareView(self, x=0, y=0, p=0):

        self.fitInView(
                self.output, 
                QtCore.Qt.KeepAspectRatio)

    def goto(
            self, 
            digit=None, 
            x=0., 
            y=0.
            ):

        e=self.m_model.element(1)
        c=e.render()
        self.player.setMedia(c)
        self.player.play()

    def open(self, *arg, **kwargs):

        print(*arg, **kwargs)
        pos=kwargs.get('position', None)
        if pos:
            p=kwargs.get('page', None)
            loc=self.getLocation(pos)
            if type(loc)==tuple:
                x, y = loc
                self.goto(p, x, y)
            elif type(loc)==list:
                topLeft=loc[0].topLeft() 
                x, y = topLeft.x(), topLeft.y()
                self.goto(p, x, y)

    def getLocation(self, loc=None):

        if not loc:
            x, y = self.getPosition()
            x, y = str(x), str(y)
            return ':'.join([x, y])
        elif type(loc)==list:
            t=[]
            for i in loc: 
                x=str(i.x())[:6]
                y=str(i.y())[:6]
                w=str(i.width())[:6]
                h=str(i.height())[:6]
                t+=[f'{x}:{y}:{w}:{h}']
            return '_'.join(t)
        elif type(loc)==str:
            l=loc.split(':')
            f=float
            if len(l)==2:
                return f(l[0]), f(l[1])
            else:
                t=[]
                for i in loc.split('_'):
                    r=QtCore.QRectF
                    x, y, w, h = tuple(i.split(':'))
                    t+=[r(f(x), f(y), f(w), f(h))]
                return t

    def on_itemAdded(self, item):
        pass

    def setVisiblePage(self):
        pass
