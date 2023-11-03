from PyQt5 import QtWidgets
from gizmo.widget.view import RenderMixin, TileMixin, BaseItem 

class PdfFitzItem(
        TileMixin,
        RenderMixin,
        BaseItem,
        QtWidgets.QGraphicsObject,
        ):
    pass
