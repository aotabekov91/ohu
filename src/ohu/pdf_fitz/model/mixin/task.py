class SearchTask(Base):
    raise

    def run(self):

        for i, e in self.m_elements.items():
            f=e.search(text)
            if f:
                self.searchFound.emit(e, f)
