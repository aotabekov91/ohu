from PyQt5 import QtWidgets
from gizmo.vimo.view.base import View
from gizmo.vimo.view.mixin import PoolItems, Zoom, MoveScene, Highlight, Select, XYPos, Copy

from ..item import FitzItem
from .mixin import Search, Outline, Hint, Links, Locate

class FitzView(
        Zoom, 
        Hint,
        Copy,
        XYPos, 
        Links,
        Search, 
        Locate,
        Select,
        Outline,
        Highlight,
        PoolItems, 
        MoveScene, 
        View,
        QtWidgets.QGraphicsView,
        ):

    canAnnotate=True
    item_class=FitzItem
