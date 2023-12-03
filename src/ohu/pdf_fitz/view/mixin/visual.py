from gizmo.utils import tag

class Visual:

    hasVisual=True

    def event_functor(self, e, ear):
        t=e.text()
        sm=self.submode()
        v=self.app.handler.view()
        if sm in ['hint', 'jump'] and t: 
            self.key+=t
            v.updateHint(self.key)
            return True

    def selectHint(
            self, sel, submode=None):

        i=sel['item']
        if submode=='jump': 
            self.jump(sel)
        elif submode=='hint':
            self.select(i, sel)

    def jump(self, sel):

        s=self.selection()
        if not s: return
        i=sel['item']
        e=i.element()
        e.jumpToBlock(s, sel)

    def visualGoTo(self, kind, digit=1):

        for i in range(digit):
            s=self.selection()
            if not s: return
            i=s['item']
            e=i.element()
            e.updateBlock(kind, s)
            i.update()

    @tag('w', modes=['visual[hint]|^own', 'visual[jump]|^own'])
    def hintWord(self):
        self.hint(kind='words')

    def visualGoToUp(self, digit=1):
        self.visualGoTo('up', digit=digit)

    def visualGoToDown(self, digit=1):
        self.visualGoTo('down', digit=digit)

    def visualGoToLeft(self, digit=1):
        self.visualGoTo('right', digit=digit)

    def visualGoToRight(self, digit=1):
        self.visualGoTo('left', digit=digit)

    @tag('o', modes=['visual[select]|^own'])
    def visualGoToFirst(self): 
        self.visualGoTo(kind='first')

    @tag('$', modes=['visual[select]|^own'])
    def visualGoToEnd(self):
        self.visualGoTo(kind='last')
