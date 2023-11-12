import fitz
from gizmo.vimo.item import mixin

class Select(mixin.Select):

    def select(self, s=[], **kwargs):

        if type(s) != list:
            s=[s]
        for i in s:
            self.setSelectionText(s)

    def setSelectionText(self, s):

        s['text']=''
        e=self.element()
        text=


