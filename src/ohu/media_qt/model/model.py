from PyQt5 import QtCore
from gizmo.widget.model import DirMixin, ElementMixin, BaseModel

from .element import MediaQtElement

class MediaQtModel(
        DirMixin,
        ElementMixin,
        BaseModel,
        QtCore.QObject
        ):

    kind='media'
    pattern='.*(mp4|mkv|avi)$'
    element_class=MediaQtElement
