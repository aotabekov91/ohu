class Copy:

    canCopy=True

    def copy(self):

        c=self.__class__(
               name=self.name,
               index=self.index,
               config=self.config,
               source=self.source)
        c.setModel(self.m_model)
        self.app.handler.connectView(c)
        idx=self.currentIndex()
        path=self.m_model.filePath(idx)
        idx=self.m_model.getPathIndex(path)
        c.setRootIndex(idx)
        return c
