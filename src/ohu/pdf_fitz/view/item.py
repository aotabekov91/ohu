from PyQt5 import QtWidgets
from gizmo.vimo.item import Render, Zoom, Item 

class PdfFitzItem(
        Render,
        Zoom,
        Item,
        QtWidgets.QGraphicsObject,
        ):
    pass
