from PyQt5 import QtWidgets
from gizmo.vimo import item

from . import mixin

class FitzItem(
        mixin.Links,
        item.mixin.Zoom, 
        item.mixin.Select,
        item.mixin.Annotate,
        item.mixin.Highlight, 
        mixin.RenderItem, 
        QtWidgets.QGraphicsObject,
        ):
    pass
