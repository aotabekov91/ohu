from plug.qt.plugs.render import DisplayRender

from .view import MediaQtView
from .model import MediaQtModel

class MediaQt(DisplayRender):

    view_class=MediaQtView
    model_class=MediaQtModel
