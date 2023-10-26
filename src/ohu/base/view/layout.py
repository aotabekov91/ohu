from .utils.single import SinglePage

class Layout:

    def __init__(
            self, 
            view,
            config={},
            mode='SinglePage',
            modes={'SinglePage': SinglePage},
            ):

        self.modes=modes
        self.m_mode=modes[mode](config)

    def layoutMode(self): 
        return self.m_mode

    def leftIndex(self, idx, count): 
        return self.m_mode.leftIndex(idx)

    def rightIndex(self, idx, count): 
        return self.m_mode.rightIndex(idx, count)

    def upIndex(self, idx, count): 
        return self.m_mode.upIndex(idx, count)

    def downIndex(self, idx, count): 
        return self.m_mode.downIndex(idx, count)

    def width(self, width): 
        return self.m_mode.width(width)

    def height(self, height):
        return self.m_mode.height(height)

    def next(self, idx, count): 
        return self.m_mode.next(idx, count)

    def prev(self, idx, count): 
        return self.m_mode.prev(idx, count)

    def current(self, idx, count):
        return self.m_mode.current(idx, count)

    def load(
            self, 
            items, 
            left=0., 
            right=0, 
            height=0.,
            rightToLeft=False, 
            ):

        return self.m_mode.load(
                items, 
                left, 
                right, 
                height,
                rightToLeft)
