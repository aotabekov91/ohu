from os.path import abspath
from PyQt5.QtWidgets import QFileSystemModel

class FileBrowserModel(QFileSystemModel):

    kind='files'
    root_path='/'

    def __init__(self, source='/'):

        super().__init__()
        self.m_data=source
        self.m_source=source
        self.setRootPath(self.root_path)

    def getPathIndex(self, path=None):

        path = path or abspath('.')
        return self.index(path)

    def element(self, idx):

        idx=idx or self.currentIndex()
        return self.filePath(idx)
