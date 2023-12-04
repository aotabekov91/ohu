from gizmo.vimo.view import mixin

class AnnotateLocate(mixin.Locate):

    canAnnotate=True

    def openAnnotationLocator(self, data={}, **kwargs):

        b=data.get('box', None)
        p=data.get('page', None)
        v=self.app.handler.type()
        if all([v, p, b]):
            tl=b[0].topLeft()
            v.goTo(p, tl.x(), tl.y())
