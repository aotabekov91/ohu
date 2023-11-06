from plug.qt.plugs.render import DisplayRender

from .view import FitzView
from .model import FitzModel

class PdfFitz(DisplayRender):

    view_class=FitzView
    model_class=FitzModel
