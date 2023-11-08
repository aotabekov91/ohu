from PyQt5 import QtWidgets
from gizmo.vimo.item import Render, Zoom, Item, Highlight, Select

from .mixin import Links

class FitzItem(
        Render, 
        Zoom, 
        Select,
        Links,
        Highlight, 
        Item,
        QtWidgets.QGraphicsObject,
        ):
    pass
