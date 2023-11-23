from plug.qt.plug import Plug

from .view import FitzView
from .model import FitzModel

class PdfFitz(Plug):

    def setup(self):

        super().setup()
        self.app.handler.addView(
                FitzView)
        self.app.handler.addModel(
                FitzModel)
