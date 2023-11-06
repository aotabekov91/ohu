import os
import fitz
import hashlib
from PyQt5 import QtCore
from gizmo.vimo.model.base import Model
from gizmo.vimo.model.mixin import Element

from ..element import FitzElement

class FitzModel(
        Element,
        Model,
        QtCore.QObject,
        ):

    kind='document'
    pattern='.*pdf$'
    element_class=FitzElement

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

    def load(self):

        s=self.m_source
        self.m_data=fitz.open(s)
        super().load()
