from PyQt5.QtCore import Qt 
from ohu.base.view.cursor import Cursor as Base

class Cursor(Base):

    def setup(self):

        super().setup()
        self.start=None

    def on_mouseMove(self, view, item, event): 
        self.move(event, item)

    def on_mouseRelease(self, view, item, event): 
        item.setCursor(item.prev_cursor)

    def on_mousePress(self, view, item, event):

        e=item.element()
        item.prev_cursor=item.cursor()
        item.setCursor(Qt.IBeamCursor)
        p=item.mapToPage(
                event.pos(), unify=False)
        self.start=e.getRow(p)

    def on_doubleClick(self, view, item, event):

        s=[]
        e=item.element()
        p=item.mapToPage(
                event.pos(), unify=False)
        data=e.getRow(p)
        if data: s+=[data] 
        item.select(s)

    def move(self, event, item):

        s=self.start
        p=item.mapToPage(
                event.pos(), unify=False)
        e=item.element()
        c=e.getRow(p)
        if s and c:
            s=e.getRows(s['box'][0], c['box'][0])
            item.select([s])
