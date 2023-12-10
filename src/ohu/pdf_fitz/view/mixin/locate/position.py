from gizmo.vimo.view import mixin

class PLocate(mixin.Locate):

    def openPositionLocator(self, data={}, **kwargs):

        p=data.get('position', None)
        i, x, y = self.parsePositionLocator(p)
        self.goTo(i, x, y)
        return i, x, y

    def getPositionLocator(self, data={}, **kwargs):

        i, x, y = self.getPosition()
        i = str(i)[:10]
        x = str(x)[:10]
        y = str(y)[:10]
        data['position'] = ':'.join([i, x, y])
        return self.createLocator(data)

    def setPositionLocator(self, data={}, **kwargs):

        i, x, y = self.openPositionLocator(data)
        self.setCurrentIndex(i)

    def parsePositionLocator(self, data=None):

        if data:
            t=data.split(':')
            i=int(t[0])
            x=float(t[1])
            y=float(t[2])
            return i, x, y
