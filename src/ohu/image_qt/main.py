from plug.qt.plugs.render import DisplayRender

from .view import ImageQtView
from .model import ImageQtModel

class ImageQt(DisplayRender):

    view_class=ImageQtView
    model_class=ImageQtModel
