from plug.qt.plugs.render import Render

from .view import FitzView
from .model import FitzModel

class PdfFitz(Render):

    unique=False
    view_class=FitzView
    model_class=FitzModel
    view_position='display'
