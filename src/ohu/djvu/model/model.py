import os
import djvu
import hashlib
from PyQt5 import QtCore, QtGui
from gizmo.widget.model import ElementMixin, BaseModel

from .element import Element

class DjvuModel(
        ElementMixin,
        BaseModel,
        QtCore.QObject
        ):

    kind='document'
    pattern='.*djvu$'
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
            dhash=shash.hexdigest()
            self.setId(dhash)

    def load(self, source):

        d=djvu.decode
        self.m_url=d.FileURI(source)
        self.m_context=d.Context().new_document(
                self.m_url)
        self.m_context.decoding_job.wait()
        self.m_data=self.m_context.pages
        super().load()
