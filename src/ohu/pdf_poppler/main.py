import os
import hashlib
from plug.qt.plugs.render import Render

from .view import PdfView
from .model import PdfModel

class PdfPoppler(Render):

    def initiate(self):

        super().initiate(
                view_class=PdfView, 
                model_class=PdfModel)

    def setId(self, source, model):

        if os.path.isfile(source):
            source=os.path.expanduser(source)
            shash = hashlib.md5()
            with open(source, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    shash.update(chunk)
                    chunk = f.read(4096)
            dhash=shash.hexdigest()
            model.setId(dhash)

    def isCompatible(self, source):
        
        if source:
            source=source.lower()
            return source.endswith('pdf')
        return super().isCompatible(source)
