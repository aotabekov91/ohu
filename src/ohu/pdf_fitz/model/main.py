import os
import fitz
import hashlib
from PyQt5 import QtCore
from gizmo.vimo.model import Model
from gizmo.vimo.model.mixin import Element

from . import mixin
from ..element import FitzElement

class FitzModel(
        mixin.AnnotateLocate,
        mixin.Locate,
        mixin.Outline,
        Element,
        Model,
        QtCore.QObject,
        ):

    isType=True
    kind='document'
    pattern='.*pdf$'
    canAnnotate=True
    wantView=['FitzView']
    element_class=FitzElement

    def setup(self):

        super().setup()
        self.assignId(self.m_source)

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
