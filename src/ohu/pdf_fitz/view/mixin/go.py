from gizmo.vimo.view import mixin

class Go(mixin.Go):

    def go(self, kind, *args, **kwargs):

        if kind=='first':
            self.goto(1)
        elif kind=='last':
            self.goto(self.count())
        elif type(kind)==int:
            self.goto(kind)
        elif kind=='next':
            self.nextItem(*args, **kwargs)
        elif kind=='prev':
            self.prevItem(*args, **kwargs)
