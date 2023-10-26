import os
import hashlib
from ohu.base import Render

from .view import View
from .model import Model

class PdfRender(Render):

    def initiate(self):

        super().initiate(
                view=View, model=Model)

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
