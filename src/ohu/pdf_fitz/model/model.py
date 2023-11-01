import os
import fitz
import hashlib
from PyQt5 import QtCore
from gizmo.widget.model import ElementMixin, BaseModel

from .element import Element

class PdfModel(
        ElementMixin,
        BaseModel,
        QtCore.QObject,
        ):

    kind='document'
    pattern='.*pdf$'
    element_class=Element

    def assignId(self, source):

        if os.path.isfile(source):
            source=os.path.expanduser(source)
            shash = hashlib.md5()
            with open(source, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    shash.update(chunk)
                    chunk = f.read(4096)
            idx=shash.hexdigest()
            self.setId(idx)

    def load(self, source):

        self.m_data=fitz.open(source)
        super().load()
