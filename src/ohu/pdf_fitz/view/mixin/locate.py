from gizmo.vimo.view import mixin

class Locate(mixin.Locate):

    def openPositionLocator(self, data):

        x, y = 0, 0
        i=data.get('page', 1)
        p=data.get('position', None)
        l=self.parsePositionLocator(p)
        if l and len(l)==3: 
            i, x, y = l
        elif l and len(l)==2: 
            x, y = l
        self.goto(i, x, y)
        return i, x, y

    def getPositionLocator(self, data=None):

        i, x, y = self.getPosition()
        i = str(i)[:10]
        x = str(x)[:10]
        y = str(y)[:10]
        return {'position': ':'.join([i, x, y])}

    def setPositionLocator(self, data=None):

        i, x, y = self.openPositionLocator(data)
        self.setCurrentIndex(i)

    def parsePositionLocator(self, data=None):

        if data:
            t=data.split(':')
            if len(t)==3:
                i=int(t[0])
                x=float(t[1])
                y=float(t[2])
                return i, x, y
            if len(t)==2:
                x=float(t[0])
                y=float(t[1])
                return x, y
