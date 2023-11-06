class Select:

    canSelect=True
    def selection(self, idx=None):

        idx = idx or self.m_curr
        item=self.item(idx)
        if item:
            return item.selection()

    def select(self, data):

        for i, r in data:
            i.select(r)
        self.redraw()

    def deselect(self, data=None):

        if data:
            for i, r in data:
                i.deselect(r)
            self.redraw()
        else:
            self.clear()

    def clear(self):

        for j, i in self.getItems():
            i.deselect()
        self.redraw()
