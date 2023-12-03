from gizmo.utils import tag
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QAbstractItemView as V

class Visual:

    hasVisual=True

    @tag('w', modes=['visual[hint]|^own', 'visual[jump]|^own'])
    def hintWord(self):
        self.hint(kind='words')

    def startHint(self, submode):
        self.hint()

    def setMode(self):

        sm=self.app.moder.submode()
        if sm=='select':
            self.setSelectionMode(V.MultiSelection)
        else:
            self.setSelectionMode(V.SingleSelection)

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

        self.setMode()
        for i in range(digit):
            m=self.selectionModel()
            idx=self.currentIndex()
            selected=m.isSelected(idx)
            self.go(kind=kind, digit=digit)
            if selected: 
                m.select(idx, QItemSelectionModel.Select)

    def visualGoToUp(self, digit=1):
        self.visualGoTo('up', digit)

    def visualGoToDown(self, digit=1):
        self.visualGoTo('down', digit)

    def visualGoToLeft(self, digit=1):
        self.visualGoTo('right', digit=digit)

    def visualGoToRight(self, digit=1):
        self.visualGoTo('left', digit=digit)
