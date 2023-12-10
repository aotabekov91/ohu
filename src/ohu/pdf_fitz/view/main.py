from gizmo.vimo import view
from PyQt5.QtWidgets import QGraphicsView

from . import mixin
from ..item import FitzItem

class FitzView(
        mixin.Hint,
        mixin.Yank,
        mixin.Links,
        mixin.Items,
        mixin.Search, 
        mixin.Visual,
        mixin.PLocate,
        mixin.ALocate,
        view.mixin.Copy,
        view.mixin.Scale, 
        view.mixin.XYPos, 
        view.mixin.Select,
        view.mixin.SceneGo,
        view.mixin.DFullscreen,
        view.mixin.ItemsHighlight,
        view.View,
        QGraphicsView,
        ):

    canFollow=True
    item_class=FitzItem
    position={'FitzView': 'display'}
