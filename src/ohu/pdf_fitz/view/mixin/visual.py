from gizmo.utils import tag

class Visual:

    hasVisual=True

    def visualFunctor(self, e):

        t=e.text()
        sm=self.app.moder.submode()
        if sm in ['hint', 'jump'] and t: 
            self.m_hint_key+=t
            self.updateHint(self.m_hint_key)

    def startVisualMode(self, mode):

        if not self.selection():
            self.hintWord()

    def startHint(self, submode, kind):

        self.m_hint_key=''
        m=self.app.moder.mode()
        m.eatEvent=True
        m.setSubmode(submode)
        self.hint(kind=kind)
        m.eventFunctor.connect(
                self.visualFunctor)
        self.hintSelected.connect(
                self.selectHint)
        self.hintFinished.connect(
                self.finishHint)

    def finishHint(self):

        m=self.app.moder.mode()
        m.setSubmode('select')
        m.eatEvent=False
        self.app.earman.clearKeys()
        m.eventFunctor.disconnect(
                self.visualFunctor)
        self.hintFinished.disconnect(
                self.finishHint)
        self.hintSelected.disconnect(
                self.selectHint)

    def selectHint(self, sel):

        item=sel['item']
        self.app.earman.clearKeys()
        sm=self.app.moder.submode()
        if sm=='jump': 
            self.jump(item, sel)
        elif sm=='hint':
            self.select(item, sel)
        self.finishHint()

    def jump(self, item, sel):

        s=self.selection()
        e=item.element()
        e.jumpToBlock(s, sel)

    def visualGoTo(self, kind, digit=1):

        for i in range(digit):
            s=self.selection()
            if s:
                i=s['item']
                e=i.element()
                e.updateBlock(kind, s)
                i.update()

    @tag('w', modes=['visual|^own'])
    def hintWord(self):
        self.startHint('hint', 'words')

    @tag('e', modes=['visual|^own'])
    def jumpWord(self):

        if self.selection():
            self.startHint('jump', 'words')

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
