from gizmo.vimo.view import mixin

class Go(mixin.Go):

    def go(self, kind, *args, **kwargs):

        if kind=='first':
            self.goTo(1)
        elif kind=='last':
            self.goTo(self.count())
        elif type(kind)==int:
            self.goTo(kind)
        elif kind=='next':
            self.nextItem(*args, **kwargs)
        elif kind=='prev':
            self.prevItem(*args, **kwargs)
