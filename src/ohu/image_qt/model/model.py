from PyQt5 import QtCore
from gizmo.widget.model import DirMixin, ElementMixin, BaseModel

from .element import ImageQtElement

class ImageQtModel(
        DirMixin, 
        ElementMixin,
        BaseModel, 
        QtCore.QObject):

    f='|'.join([
      'png', 
      'bmp', 
      'gif', 
      'x[bp]m',
      'p[bgp]m', 
      'jp(e){0,1}g', 
      ])

    kind='img'
    pattern=f'.*({f})$'
    element_class=ImageQtElement
