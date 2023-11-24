import os
from gizmo.vimo import model

from . import mixin

class FilesModel(
        mixin.Locate,
        model.FileSystemModel
        ):

    isType=True
    kind='files'
    wantUniqView=True
    wantView=['FilesView']

    @classmethod
    def isCompatible(cls, source):
        return source and os.path.isdir(source)

    @classmethod
    def getSourceName(cls, source):
        return '/'
