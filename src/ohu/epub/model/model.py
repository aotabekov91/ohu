import os
import hashlib
from zipfile import ZipFile
from xmltodict import parse
from PyQt5 import QtGui, QtCore
from urllib.parse import unquote
from bs4 import BeautifulSoup as Soup
from gizmo.widget.model import BaseModel

from .element import EpubElement
from .utils import load, getContent

class EpubModel(
        BaseModel, 
        QtCore.QObject
        ):

    kind='document'
    pattern='.*epub$'
    element_class=EpubElement

    def setup(self):

        self.schap = {}
        self.content = []
        self.flist = None
        self.zfile = None
        self.odict = None
        super().setup()

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
        else:
            self.setId(None)

    def load(self, source):

        z, f, d, t = load(source)
        self.zfile, self.flist=z, f
        self.tdir, self.odict=t, d
        self.m_data, self.schaps = getContent(z, f, d)
        self.setElements()

    def replaceRefs(self, c):

        for f in ['src="', 'href="']:
            c=c.replace(
                    f, f'{f}{self.tdir.name}/')
        return c

    def setElements(self):

        for i, d in enumerate(self.m_data):
            j=i+1
            idx, n, c = d
            c=self.replaceRefs(c)
            e=self.element_class(
                    index=j,
                    model=self,
                    data=(idx, n, c))
            self.m_elements[j]=e
