from gizmo.vimo import model

from . import mixin

class FileBrowserModel(
        mixin.Locate,
        model.FileSystemModel
        ):
    pass

