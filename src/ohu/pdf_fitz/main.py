from plug.qt.plugs.viewer import Viewer

from .view import FitzView
from .model import FitzModel

class PdfFitz(Viewer):

    unique=False
    view_class=FitzView
    model_class=FitzModel
    view_position='display'
