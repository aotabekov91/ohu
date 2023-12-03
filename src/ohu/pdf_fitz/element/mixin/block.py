from PyQt5 import QtCore, QtGui

class Block:

    canBlock=True
    direction=[None, None]

    def changeDirection(self):

        x, y = tuple(self.direction)
        y='up' if y=='down' else 'down'
        x='left' if x=='right' else 'right'
        self.direction=[x, y]

    def getData(self, sel):

        if sel:
            b=sel['box']
            if len(b)>0: self.last=sel
            size=self.size()
            s=self.m_norm.mapRect(b[0])
            e=self.m_norm.mapRect(b[-1])
            return b, s, e, size

    def updateBlock(self, kind, sel):

        k=''
        if kind: 
            k=kind[0].title()+kind[1:] 
        n=f'block{k}'
        f=getattr(self, n, None)
        if f: f(sel)

    def blockLast(self, sel):

        self.direction[0]='right'
        b, s, e, size = self.getData(sel)
        x, y = e.x(), e.y()
        w, h = self.size().width(), e.height()
        r=(x, y, x+w, y+h)
        f=self.m_data.get_text('blocks', clip=r)
        if f:
            tl=QtCore.QPointF(f[0][0], f[0][1])
            br=QtCore.QPointF(f[0][2], f[0][3])
            r=QtCore.QRectF(tl, br)
            b[-1]=self.m_norm_inv.mapRect(r)

    def blockFirst(self, sel):

        self.direction[0]='left'
        b, s, e, size = self.getData(sel)
        x, y = 0, s.y()
        w, h = s.x()+s.width(), s.height()
        r=(x, y, x+w, y+h)
        f=self.m_data.get_text('blocks', clip=r)
        if f:
            tl=QtCore.QPointF(f[0][0], f[0][1])
            br=QtCore.QPointF(f[0][2], f[0][3])
            r=QtCore.QRectF(tl, br)
            b[0]=self.m_norm_inv.mapRect(r)

    def blockDown(self, sel):

        if sel and self.direction[1]=='up':
            self.cancelBlockUp(sel)
        else:
            b, s, e, size = self.getData(sel)
            self.updateBlock('last', sel)
            x, y = e.x(), e.y()+e.height()*1.5
            w, h = e.width(), e.height()
            r=(0, y, x+w, y+h)
            f=self.m_data.get_text('blocks', clip=r)
            self.direction[1]='down'
            if f:
                tl=QtCore.QPointF(f[0][0], f[0][1])
                br=QtCore.QPointF(f[0][2], f[0][3])
                r=QtCore.QRectF(tl, br)
                b+=[self.m_norm_inv.mapRect(r)]

    def blockUp(self, sel):

        if sel and self.direction[1]=='down':
            self.cancelBlockDown(sel)
        else:
            b, s, e, size = self.getData(sel)
            self.updateBlock('first', sel)
            x, y = s.x(), s.y()-s.height()*1.5
            w, h = s.width(), s.height()
            r=(x, y, x+w, y+h)
            f=self.m_data.get_text('blocks', clip=r)
            self.direction[1]='up'
            if f:
                tl=QtCore.QPointF(f[0][0], f[0][1])
                br=QtCore.QPointF(f[0][2], f[0][3])
                r=QtCore.QRectF(tl, br)
                b.insert(0, self.m_norm_inv.mapRect(r))

    def blockRight(self, sel):

        if sel and self.direction[0]=='left':
            self.cancelBlockLeft(sel)
        else:
            b, s, e, size = self.getData(sel)
            x, y =e.x()+e.width()+1, e.y()
            w, h = size.width(), e.height()
            r=(x, y, x+w, y+h)
            f=self.m_data.get_text('words', clip=r)
            self.direction[0]='right'
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

    def blockLeft(self, sel):

        if sel and self.direction[0]=='right':
            self.cancelBlockRight(sel)
        else:
            self.direction[0]='left'
            b, s, e, size = self.getData(sel)
            b, s, e, size = self.getData(sel)
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

    def cancelBlockDown(self, sel):

        b, s, e, size = self.getData(sel)
        if len(b)>1: 
            sel['box']=b[:-1]
        else:
            self.changeDirection()
            self.blockUp(sel)

    def cancelBlockUp(self, sel):

        b, s, e, size = self.getData(sel)
        if len(b)>1: 
            sel['box']=b[1:]
        else:
            self.changeDirection()
            self.blockDown(sel)

    def cancelBlockRight(self, sel):

        b, s, e, size = self.getData(sel)
        x, y = e.x(), e.y()
        w, h = e.width(), e.height()
        r=(x, y, x+w, h+y)
        f=self.m_data.get_text('words', clip=r)
        if len(f)<=1:
            self.changeDirection()
            self.blockLeft(sel)
        else:
            br=QtCore.QPointF(f[-2][2], f[-2][3])
            e.setBottomRight(br)
            b[-1]=self.m_norm_inv.mapRect(e)

    def cancelBlockLeft(self, sel):

        b, s, e, size = self.getData(sel)
        x, y = s.x(), s.y()
        w, h = s.width(), s.height()
        r=(x, y, x+w, h+y)
        f=self.m_data.get_text('words', clip=r)
        if len(f)<=1:
            self.changeDirection()
            self.blockRight(sel)
        else:
            tl=QtCore.QPointF(f[1][0], f[1][1])
            s.setTopLeft(tl)
            b[0]=self.m_norm_inv.mapRect(s)

    def jumpToBlock(self, csel, jsel):

        cb=csel['box']
        jb=jsel['box']
        ctl=cb[0].topLeft()
        jtl=jb[0].topLeft()
        cbr=cb[-1].bottomRight()
        jbr=jb[-1].bottomRight()

        raise
        if abs(ctl.y()-jbr.y())<0.1:
            if jtl.x()<ctl.x():
                cb[0].setTopLeft(jtl)
            elif cbr.x()<jbr.x():
                cb[0].setBottomRight(jbr)
        elif ctl.y()-jbr.y()>0.1:
            self.updateBlock('first', csel)
            b, s, e = self.getData(csel)
            self.updateBlock('last', jsel)
            b, s, e = self.getData(jsel)
            cb.insert(0, jb[0])
