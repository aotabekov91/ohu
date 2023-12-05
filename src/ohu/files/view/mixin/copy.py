class Copy:

    canCopy=True

    def copy(self):

        c=self.__class__(
                app=self.app, 
                name=self.name, 
                index=self.m_id, 
                config=self.m_config)
        c.setModel(self.m_model)
        self.app.handler.connectView(c)
        idx=self.currentIndex()
        path=self.m_model.filePath(idx)
        idx=self.m_model.getPathIndex(path)
        c.setRootIndex(idx.parent())
        c.setCurrentIndex(idx)
        return c
