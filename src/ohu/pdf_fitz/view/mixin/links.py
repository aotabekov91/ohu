import fitz
import subprocess
from PyQt5.QtCore import QPointF

class Links:

    hasLinks=True

    def openLink(self, l):

        k1=fitz.LINK_GOTO
        k2=fitz.LINK_GOTOR
        d=l['link'].dest
        if d.kind in [k1, k2]:
            raise
        elif d.kind==fitz.LINK_NAMED:
            r=self.m_model.m_data.resolve_link(
                    d.uri)
            p, x, y = r
            tl=QPointF(x, y)
            item=self.item(p+1)
            elem=item.element()
            tl=elem.m_norm_inv.map(tl)
            self.goTo(p+1, tl.x(), tl.y())
        elif d.kind==fitz.LINK_URI:
            cmd=['qutebrowser', d.uri]
            subprocess.Popen(cmd)


