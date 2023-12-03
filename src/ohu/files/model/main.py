import os
from gizmo.vimo import model

from . import mixin

class FilesModel(
        mixin.NoIcon,
        mixin.Locate,
        model.FileSystemModel
        ):

    isType=True
    kind='files'
    wantUniqView=True
    wantView=['FilesView']

    def resetConfigure(self, **kwargs):

        s=kwargs.get('source', None)
        if s: self.m_source=s
        
    @classmethod
    def isCompatible(cls, s, **kwargs):
        return s and os.path.isdir(s)

    @classmethod
    def getSourceName(cls, s, **kwargs):
        return '/'
