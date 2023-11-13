import os
from PyQt5.QtWidgets import QFileSystemModel

class FileBrowserModel(QFileSystemModel):

    kind='files'

    def getPath(self, idx=None):

        idx=idx or self.ui.currentIndex()
        p=self.filePath(idx)
        if os.path.exists(p): 
            return p
