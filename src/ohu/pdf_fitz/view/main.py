from gizmo.vimo import view
from PyQt5 import QtWidgets, QtCore

from . import mixin
from ..item import FitzItem

class FitzView(
        mixin.Hint,
        mixin.Yank,
        mixin.Links,
        mixin.Search, 
        mixin.Locate,
        mixin.Visual,
        mixin.AnnotateLocate,
        view.mixin.Copy,
        view.mixin.Scale, 
        view.mixin.XYPos, 
        view.mixin.Select,
        view.mixin.SceneGo,
        view.mixin.PoolItems, 
        view.mixin.ItemsHighlight,
        view.View,
        QtWidgets.QGraphicsView,
        ):

    item_class=FitzItem
    position={'FitzView': 'display'}
