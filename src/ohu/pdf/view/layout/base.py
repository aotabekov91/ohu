from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .single_page import SinglePage

class Layout:

    def __init__(self, documentView):

        self.s_settings=documentView.s_settings
        self.fromLayoutMode(
                self.s_settings.get(
                    'layoutMode', 'SinglePage'))

    def layoutMode(self): 
        return self.m_layoutMode

    def leftIndex(self, index): 
        return self.m_layoutMode.leftIndex(index)

    def rightIndex(self, index, count): 
        return self.m_layoutMode.rightIndex(index, count)

    def fromLayoutMode(self, layoutMode):

        layoutModes={'SinglePage': SinglePage}
        self.m_layoutMode=layoutModes[layoutMode](
                self.s_settings)

    def visibleWidth(self, viewportWidth): 
        return self.m_layoutMode.visibleWidth(viewportWidth)

    def visibleHeight(self, viewportHeight):

        pageSpacing=self.s_settings.get('pageSpacing', 0.0)
        return viewportHeight-2.0*pageSpacing

    def prepareLayout(
            self, 
            pageItems, 
            rightToLeftMode=False, 
            left=0., 
            right=0, 
            height=0.):

        return self.m_layoutMode.prepareLayout(
                pageItems, rightToLeftMode, left, right, height)

    def nextPage(self, page, count): 
        return self.m_layoutMode.nextPage(page, count)

    def previousPage(self, page, count): 
        return self.m_layoutMode.previousPage(page, count)

    def currentPage(self, page): 
        return self.m_layoutMode.currentPage(page)
