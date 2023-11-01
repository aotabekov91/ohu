from plug.qt.plugs.render import DisplayRender 

from .view import EpubView
from .model import EpubModel

class Epub(DisplayRender):

    view_class=EpubView
    model_class=EpubModel
