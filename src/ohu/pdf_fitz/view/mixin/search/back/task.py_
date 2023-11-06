from gizmo.utils import Task

class SearchTask(Task):

    def __init__(self, view):
        self.m_view=view
        super().__init__(parent=view)

    def start(self, text):

        self.text=text
        super().start()

    def run(self):

        items=self.m_view.getItems()
        for j, i in items:
            e=i.m_element
            f=e.search(self.text)
            if f: self.taskReady.emit((i, f))
        self.finished.emit()
