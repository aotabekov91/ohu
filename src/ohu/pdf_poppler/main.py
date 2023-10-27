from plug.qt.plugs.render import Render

from .view import PdfView
from .model import PdfModel

class PdfPoppler(Render):

    def initiate(self):

        super().initiate(
                view_class=PdfView, 
                model_class=PdfModel)

    def isCompatible(self, source):
        
        if source:
            source=source.lower()
            return source.endswith('pdf')
