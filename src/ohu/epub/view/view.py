from PyQt5 import QtWidgets
from gizmo.widget.view import XYMixin, ItemMixin, BaseView

class EpubView(
        XYMixin,
        ItemMixin,
        BaseView,
        QtWidgets.QTextBrowser
        ):

    scene_class=None
    cursor_class=None

    def prepareView(self, digit=1, x=0, y=0):

        item=self.item(digit)
        if item:
            e=item.element()
            idx, n, content = e.data()
            self.setHtml(content)
