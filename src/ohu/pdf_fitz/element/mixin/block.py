from PyQt5 import QtCore, QtGui

class Block:

    canBlock=True

    def updateBlock(self, kind, sel):

        b=sel['box']
        size=self.size()
        if not b: return
        s=self.m_norm.mapRect(b[0])
        e=self.m_norm.mapRect(b[-1])
        if kind == 'last':
            x, y = e.x(), e.y()
            w, h = self.size().width(), e.height()
            r=(x, y, x+w, y+h)
            f=self.m_data.get_text('blocks', clip=r)
            if f:
                tl=QtCore.QPointF(f[0][0], f[0][1])
                br=QtCore.QPointF(f[0][2], f[0][3])
                r=QtCore.QRectF(tl, br)
                b[-1]=self.m_norm_inv.mapRect(r)
        elif kind=='first':
            x, y = 0, s.y()
            w, h = s.x()+s.width(), s.height()
            r=(x, y, x+w, y+h)
            f=self.m_data.get_text('blocks', clip=r)
            if f:
                tl=QtCore.QPointF(f[0][0], f[0][1])
                br=QtCore.QPointF(f[0][2], f[0][3])
                r=QtCore.QRectF(tl, br)
                b[0]=self.m_norm_inv.mapRect(r)
        elif kind=='down':
            self.updateBlock('lastWord', sel)
            x, y = e.x(), e.y()+e.height()*1.5
            w, h = e.width(), e.height()
            r=(x, y, x+w, y+h)
            f=self.m_data.get_text('blocks', clip=r)
            if f:
                tl=QtCore.QPointF(f[0][0], f[0][1])
                br=QtCore.QPointF(f[0][2], f[0][3])
                r=QtCore.QRectF(tl, br)
                b+=[self.m_norm_inv.mapRect(r)]
        elif kind=='up':
            self.updateBlock('firstWord', sel)
            x, y = s.x(), s.y()-s.height()*1.5
            w, h = s.width(), s.height()
            r=(x, y, x+w, y+h)
            f=self.m_data.get_text('blocks', clip=r)
            if f:
                tl=QtCore.QPointF(f[0][0], f[0][1])
                br=QtCore.QPointF(f[0][2], f[0][3])
                r=QtCore.QRectF(tl, br)
                b.insert(0, self.m_norm_inv.mapRect(r))
        elif kind=='cancelDown':
            if len(b)>1: s['box']=b[:-2]
        elif kind=='cancelUp':
            if len(b)>1: s['box']=b[1:]
        elif kind=='next':
            x, y =e.x()+e.width()+1, e.y()
            w, h = size.width(), e.height()
            r=(x, y, x+w, y+h)
            f=self.m_data.get_text('words', clip=r)
            if f:
                br=QtCore.QPointF(f[0][2], f[0][3])
                e.setBottomRight(br)
                b[-1]=self.m_norm_inv.mapRect(e)
            else:
                r=(0, y+h+1, x, y+h+100)
                f=self.m_data.get_text('words', clip=r)
                if f:
                    tl=QtCore.QPointF(f[0][0], f[0][1])
                    br=QtCore.QPointF(f[0][2], f[0][3])
                    r=QtCore.QRectF(tl, br)
                    b+=[self.m_norm_inv.mapRect(r)]
        elif kind=='prev':
            x, y = s.x()-2, s.y()
            w, h = 5, s.height()
            w, h = size.width(), e.height()
            r=(0, y, x, y+h)
            f=self.m_data.get_text('words', clip=r)
            if f:
                tl=QtCore.QPointF(f[-1][0], f[-1][1])
                s.setTopLeft(tl)
                b[0]=self.m_norm_inv.mapRect(s)
            else:
                r=(0, y-100, size.width(), y)
                f=self.m_data.get_text('words', clip=r)
                if f:
                    tl=QtCore.QPointF(f[-1][0], f[-1][1])
                    br=QtCore.QPointF(f[-1][2], f[-1][3])
                    r=QtCore.QRectF(tl, br)
                    b.insert(0, self.m_norm_inv.mapRect(r))
        elif kind=='cancelNext':
            x, y = e.x(), e.y()
            w, h = e.width(), e.height()
            r=(x, y, x+w, h+y)
            f=self.m_data.get_text('words', clip=r)
            if len(f)<=1:
                sel['box']=b[:-1]
            else:
                br=QtCore.QPointF(f[-2][2], f[-2][3])
                e.setBottomRight(br)
                b[-1]=self.m_norm_inv.mapRect(e)
        elif kind=='cancelPrev':
            x, y = s.x(), s.y()
            w, h = s.width(), s.height()
            r=(x, y, x+w, h+y)
            f=self.m_data.get_text('words', clip=r)
            if len(f)<=1:
                sel['box']=b[:-1]
            else:
                tl=QtCore.QPointF(f[1][0], f[1][1])
                s.setTopLeft(tl)
                b[0]=self.m_norm_inv.mapRect(s)

    def jumpToBlock(self, csel, jsel):

        cb=csel['box']
        jb=jsel['box']
        ctl=cb[0].topLeft()
        cbr=cb[-1].bottomRight()
        jtl=jb[0].topLeft()
        jbr=jb[-1].bottomRight()

        print(ctl, jbr)
        if abs(ctl.y()-jbr.y())<0.1:
            if jtl.x()<ctl.x():
                cb[0].setTopLeft(jtl)
            elif cbr.x()<jbr.x():
                cb[0].setBottomRight(jbr)
        elif ctl.y()-jbr.y()>0.1:
            self.updateBlock('first', csel)
            self.updateBlock('last', jsel)
            cb.insert(0, jb[0])
            raise


        # s=self.view.selection()
        # item=s[-1]['item']
        # elem=item.element()
        # # b=self.s[0]['box']
        # # start, end, rect = b[0], b[-1], 
        # start=self.s[0]['box'][0]
        # end=self.s[0]['box'][-1]
        # rect=s[0]['box'][0]
        # if rect.y()>end.y():
        #     # item.select([page.getRows(start, rect)])
        #     selected=[elem.getRows(start, rect)]
        # elif rect.y()<start.y():
        #     # item.select([page.getRows(rect, end)])
        #     selected=[elem.getRows(rect, end)]
        # else:
        #     # item.select([page.getRows(start, rect)])
        #     selected=[elem.getRows(start, rect)]
        # item.select(selected)
        # self.hintSelected.disconnect(self.jump)
