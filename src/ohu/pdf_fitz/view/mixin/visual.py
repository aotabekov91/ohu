from gizmo.utils import tag

class Visual:

    hasBlocks=True

    def setup(self):

        super().setup()
        self.hintSelected.connect(
                self.selectHinted)
        self.app.moder.plugsLoaded.connect(
                self.saveVisual)

    def saveVisual(self, plugs):
        self.visual=plugs.get('visual', None)

    def selectHinted(self, sel):

        if self.visual.submode()=='hint':
            i=sel['item']
            sm=self.submode()
            if sm=='Jump': 
                self.jump(sel)
            elif sm=='hint':
                self.view.select(i, sel)

    def jump(self, sel):

        i=sel['item']
        e=i.element()
        c=self.view.selection()
        e.jumpToBlock(c, sel)

    def visualGoTo(self, kind, digit=1):

        for i in range(digit):
            s=self.view.selection()
            if not s: return
            i=s['item']
            e=i.element()
            e.updateBlock(kind, s)
            i.update()

    @tag('w', modes=['visual[hint]|^own'])
    def hintWord(self):

        self.key=''
        self.hint(kind='words')

    def getSelection(self):

        v=self.app.handler.view()
        return v.selection()

    def visualGoToUp(self, digit=1):

        sel=self.getSelection()
        if sel:
            raise
        else:
            self.goToUp(digit)

    @tag('w', modes=['visual[Jump]|^own']) 
    def jumpWord(self):
        self.hintWord()

    @tag('o', modes=['visual[Select]|^own'])
    def visualGoToStart(self): 
        self.visualGoTo(kind='first')

    @tag('$', modes=['visual[Select]|^own'])
    def visualGoToEnd(self):
        self.visualGoTo(kind='last')

    @tag('w', modes=['visual[Select]|^own']) 
    def visualGoToWord(self, digit=1):
        self.visualGoTo(kind='next', digit=digit)
        
    @tag('W', modes=['visual[Select]|^own'])
    def visualDegoToWord(self, digit=1):
        self.visualGoTo(kind='cancelNext', digit=digit)

    @tag('b', modes=['visual[Select]|^own']) 
    def visualBackToWord(self, digit=1):
        self.visualGoTo(kind='prev', digit=digit)
        
    @tag('B', modes=['visual[Select]|^own']) 
    def deselectPrev(self, digit=1):
        self.visualGoTo(kind='cancelPrev', digit=digit)
