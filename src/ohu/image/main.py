from plug.qt.plugs.render import Render

from .view import ImageView
from .model import ImageModel

class Image(Render):

    def initiate(self):
        super().initiate(ImageView, ImageModel)

    def isCompatible(self, source):
        
        if source:
            s=source.lower()
            return s.endswith('jpg')

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
