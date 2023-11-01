from plug.qt.plugs.render import DisplayRender

from .view import PdfView
from .model import PdfModel

class PdfFitz(DisplayRender):

    view_class=PdfView
    model_class=PdfModel
