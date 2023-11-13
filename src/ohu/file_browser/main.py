import os
from plug.qt.plugs.viewer import Viewer

from .view import FileBrowserView
from .model import FileBrowserModel

class FileBrowser(Viewer):

    unique=True
    position='dock_left'
    view_class=FileBrowserView
    model_class=FileBrowserModel

    def isCompatible(self, s):
        return s and os.path.isdir(s)
