from gizmo.utils import tag

class Visual:

    hasBlocks=True

    def getSelection(self):

        v=self.app.handler.view()
        if v: return v.selection()

    def startHint(self):
        pass

    def finishHint(self):
        pass

    def selectHint(
            self, sel, submode=None):

        i=sel['item']
        if submode=='jump': 
            self.jump(sel)
        elif submode=='hint':
            self.select(i, sel)

    def jump(self, sel):

        i=sel['item']
        e=i.element()
        c=self.selection()
        e.jumpToBlock(c, sel)

    def visualGoTo(self, kind, digit=1):

        for i in range(digit):
            s=self.selection()
            if not s: return
            i=s['item']
            e=i.element()
            e.updateBlock(kind, s)
            i.update()

    def visualGoToUp(self, digit=1):
        self.visualGoTo('up', digit=digit)

    def visualGoToDown(self, digit=1):
        self.visualGoTo('down', digit=digit)

    def visualGoToLeft(self, digit=1):

        sel=self.getSelection()
        if sel: raise

    def visualGoToRight(self, digit=1):

        sel=self.getSelection()
        if sel: raise

    @tag('w', modes=['visual[hint]|^own'])
    def hintWord(self):
        self.hint(kind='words')

    @tag('w', modes=['visual[hint]|^own'])
    def hintWord(self):
        self.hint(kind='words')

    @tag('w', modes=['visual[jump]|^own']) 
    def jumpWord(self):
        self.hintWord()

    @tag('o', modes=['visual[select]|^own'])
    def visualGoToStart(self): 
        self.go(kind='start')

    @tag('$', modes=['visual[select]|^own'])
    def visualGoToEnd(self):
        self.visualGoTo(kind='last')

    @tag('w', modes=['visual[select]|^own']) 
    def visualGoToWord(self, digit=1):
        self.visualGoTo(kind='next', digit=digit)
        
    @tag('W', modes=['visual[select]|^own'])
    def visualDegoToWord(self, digit=1):
        self.visualGoTo(kind='cancelNext', digit=digit)

    @tag('b', modes=['visual[select]|^own']) 
    def visualBackToWord(self, digit=1):
        self.visualGoTo(kind='prev', digit=digit)
        
    @tag('B', modes=['visual[select]|^own']) 
    def deselectPrev(self, digit=1):
        self.visualGoTo(kind='cancelPrev', digit=digit)
