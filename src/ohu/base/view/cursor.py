from PyQt5.QtCore import QObject, Qt 

class Cursor(QObject):

    def __init__(self, view): 

        self.start=None
        super().__init__(view)
        view.itemMouseMoveOccured.connect(
                self.on_mouseMove)
        view.itemMousePressOccured.connect(
                self.on_mousePress)
        view.itemMouseReleaseOccured.connect(
                self.on_mouseRelease)
        view.itemMouseDoubleClickOccured.connect(
                self.on_doubleClick)

    def move(self, event, item):

        s=self.start
        point=item.mapToPage(
                event.pos(), unify=False)
        c=item.page().getRow(point)
        if s and c:
            s=item.page().getRows(
                    s['box'][0], c['box'][0])
            item.select([s])

    def on_mousePress(
            self, view, item, event):

        page=item.page()
        item.prev_cursor=item.cursor()
        item.setCursor(Qt.IBeamCursor)
        point=item.mapToPage(
                event.pos(), 
                unify=False)
        self.start=page.getRow(
                point)

    def on_mouseMove(
            self, view, item, event): 
        self.move(event, item)

    def on_mouseRelease(
            self, view, item, event): 
        item.setCursor(item.prev_cursor)

    def on_doubleClick(
            self, view, item, event):

        s=[]
        page=item.page()
        point=item.mapToPage(
                event.pos(), 
                unify=False
                )
        data=page.getRow(point)
        if data: s+=[data] 
        item.select(s)
