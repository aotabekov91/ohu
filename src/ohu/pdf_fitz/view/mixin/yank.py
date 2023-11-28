class Yank:

    canYank=True

    def yank(self):

        s=self.selection()
        if not s:  return
        print(s)
        raise
        t=[]
        for s in s: 
            t+=[s['text']]
        clip=self.app.qapp.clipboard()
        clip.setText(' '.join(t))
        self.select()
        self.refresh()
