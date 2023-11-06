class Search:

    def setup(self):

        super().setup()
        self.m_search_cache={}

    def search(self, txt):

        c=self.m_search_cache.get(txt, None)
        if c: return c
        return self.m_data.search_for(txt)
