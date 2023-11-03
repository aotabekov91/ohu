from PyQt5 import QtWidgets
from gizmo.widget.view import TileMixin, RenderMixin, BaseItem

class ImageQtItem(
        TileMixin,
        RenderMixin,
        BaseItem,
        QtWidgets.QGraphicsObject
        ):
    pass
