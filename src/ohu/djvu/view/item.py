from PyQt5 import QtWidgets
from gizmo.widget.view import TileMixin, RenderMixin, BaseItem

from .tile import Tile

class DjvuItem(
        TileMixin,
        RenderMixin,
        BaseItem,
        QtWidgets.QGraphicsObject,
        ):
    pass
