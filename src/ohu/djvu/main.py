from plug.qt.plugs.render import DisplayRender

from .view import DjvuView
from .model import DjvuModel

class DjvuLibre(DisplayRender):

    view_class=DjvuView
    model_class=DjvuModel
