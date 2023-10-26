class SinglePage:

    def __init__(self, config):

        self.config=config
        self.viewportPadding=config.get('viewportPadding', 0) 

    def width(self, width):

        pageSpacing=self.config.get('pageSpacing', 0.0)
        return width-self.viewportPadding-2.*pageSpacing

    def height(self, height):

        pageSpacing=self.config.get('pageSpacing', 0.0)
        return height-2.0*pageSpacing

    def leftIndex(self, idx, count): 
        return idx

    def rightIndex(self, idx, count): 
        return idx

    def upIndex(self, idx, count): 
        return idx

    def downIndex(self, idx, count): 
        return idx

    def next(self, idx, count): 
        return min(idx+1, count)

    def prev(self, idx, count): 
        return max(idx-1, 1)

    def current(self, idx, count): 
        return idx

    def load(
            self, 
            items, 
            left, 
            right, 
            height,
            rightToLeft, 
            ):

        pageSpacing=self.config.get('pageSpacing', 0.0)
        pageHeight=0.
        for page in items:
            boundingRect=page.boundingRect()
            left=-boundingRect.left()-0.5*boundingRect.width()
            top=height-boundingRect.top()
            page.setPos(left, top)
            pageHeight=boundingRect.height()
            left=min(left, -0.5*boundingRect.width())#-pageSpacing)
            right=max(right, 0.5*boundingRect.width())#+pageSpacing)
            height+=pageSpacing+pageHeight
        return left, right, height
