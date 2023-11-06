from PyQt5 import QtWidgets
from gizmo.vimo.item import Render, Zoom, Item 

from .select import Select

class FitzItem(
        Render, Zoom, Select, Item,
        QtWidgets.QGraphicsObject,
        ):
    pass
