from PyQt5 import QtWidgets
from gizmo.vimo.item import RenderItem
from gizmo.vimo.item.mixin import Zoom, Highlight, Select, Annotate

from .mixin import Links

class FitzItem(
        Zoom, 
        Links,
        Select,
        Annotate,
        Highlight, 
        RenderItem, 
        QtWidgets.QGraphicsObject,
        ):
    pass
