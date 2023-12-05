from gizmo.vimo.view import mixin

class Go(mixin.ViewGo):
    
    def go(self, *args, **kwargs):

        super().go(*args, **kwargs)
        self.update()

    def goTo(self, digit=None, **kwargs):

        if type(digit)==int:
            pidx=self.currentIndex().parent()
            idx=self.m_model.index(digit-1, 0, pidx)
            self.setCurrentIndex(idx)
        else:
            super().goTo(digit=digit, **kwargs)

    def goToLast(self):

        pidx=self.currentIndex().parent()
        rcount=self.m_model.rowCount(pidx)
        idx=self.m_model.index(rcount-1, 0, pidx)
        self.setCurrentIndex(idx)

    def goToFirst(self):

        pidx=self.currentIndex().parent()
        idx=self.m_model.index(0, 0, pidx)
        self.setCurrentIndex(idx)

    def goToRight(self, digit=1):
        
        for i in range(digit):
            idx=self.currentIndex()
            if self.m_model.isDir(idx):
                c=self.m_model.index(0, 0, idx)
                self.setCurrentIndex(c)
                self.setRootIndex(idx)
                path=self.m_model.filePath(idx)
                self.m_model.setId(path)
                self.modelChanged.emit(self.m_model)

    def goToLeft(self, digit=1):

        for i in range(digit):
            r=self.rootIndex()
            p=r.parent()
            if p: 
                self.setRootIndex(p)
                self.setCurrentIndex(r)
                path=self.m_model.filePath(p)
                self.m_model.setId(path)
                self.modelChanged.emit(self.m_model)

    def setRootIndex(self, idx):

        super().setRootIndex(idx)
        rc=self.m_model.rowCount(idx)
        for i in range(rc):
            c=self.m_model.index(i, 0, idx)
            p=self.m_model.filePath(c)
            i=self.m_model.index(p)
            if self.m_model.canFetchMore(i):
                self.m_model.fetchMore(i)
