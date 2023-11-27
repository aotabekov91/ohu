from PyQt5 import QtWidgets
from gizmo.vimo import view

from . import mixin
from ..item import FitzItem

class FitzView(
        mixin.Go,
        mixin.Hint,
        mixin.Links,
        mixin.Search, 
        mixin.Locate,
        mixin.AnnotateLocate,
        view.mixin.Copy,
        view.mixin.Scale, 
        view.mixin.XYPos, 
        view.mixin.Select,
        view.mixin.PoolItems, 
        view.mixin.MoveScene, 
        view.mixin.ItemsHighlight,
        view.View,
        QtWidgets.QGraphicsView,
        ):

    canAnnotate=True
    item_class=FitzItem
    position={'FitzView': 'display'}
