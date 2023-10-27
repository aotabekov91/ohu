from plug.qt.plugs.render import Render as Base

class Render(Base):

    def readSource(self, source):

        if self.isCompatible(source):
            return self.model_class(
                    source=source)

    def getView(self, model):

        if model:
            source=model.source()
            if self.isCompatible(source):
                view=self.view_class(self.app)
                view.setModel(model)
                return view
