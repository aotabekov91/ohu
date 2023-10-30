import re
from plug.qt.plugs.render import Render

from .view import ImageQtView
from .model import ImageQtModel

class ImageQt(Render):

    def initiate(self):
        f='|'.join([
          'png', 
          'bmp', 
          'gif', 
          'x[bp]m',
          'p[bgp]m', 
          'jp(e){0,1}g', 
          ])
        super().initiate(
                f'.*({f})$',
                ImageQtView, 
                ImageQtModel,
                )
        print(self.pattern)

    def setView(self, view, **kwargs):

        self.app.display.open(
                view, **kwargs)

    def getView(self, model, **kwargs):

        d=self.app.display
        config=d.getRenderConfig(self)
        v=self.view_class(
                app=self.app, 
                config=config, 
                **kwargs)
        v.setModel(model)
        return v

    def getModel(self, source, **kwargs):

        m=self.app.buffer.get(source)
        if not m:
            m = super().getModel(
                    source, **kwargs)
            self.app.buffer.set(source, m)
        return m
