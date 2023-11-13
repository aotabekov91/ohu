from plug.qt.plugs.viewer import Viewer

from .view import FitzView
from .model import FitzModel

class PdfFitz(Viewer):

    unique=False
    position='display'
    view_class=FitzView
    model_class=FitzModel
