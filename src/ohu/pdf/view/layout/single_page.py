from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class SinglePage:

    def __init__(self, settings):

        self.s_settings=settings
        self.viewportPadding=settings.get('viewportPadding', 0) 

    def visibleWidth(self, viewportWidth):

        pageSpacing=self.s_settings.get('pageSpacing', 0.0)
        return viewportWidth-self.viewportPadding#-2.*pageSpacing

    def prepareLayout(
            self, 
            pageItems, 
            rightToLeftMode, 
            left, 
            right, 
            height):

        pageSpacing=self.s_settings.get('pageSpacing', 0.0)
        pageHeight=0.
        for page in pageItems:
            boundingRect=page.boundingRect()
            left=-boundingRect.left()-0.5*boundingRect.width()
            top=height-boundingRect.top()
            page.setPos(left, top)
            pageHeight=boundingRect.height()
            left=min(left, -0.5*boundingRect.width())#-pageSpacing)
            right=max(right, 0.5*boundingRect.width())#+pageSpacing)
            height+=pageSpacing+pageHeight
        return left, right, height

    def leftIndex(self, index): 
        return index

    def rightIndex(self, index, count): 
        return index

    def nextPage(self, page, count): 
        return min(page+1, count)

    def previousPage(self, page, count): 
        return max(page-1, 1)

    def currentPage(self, page): 
        return page
