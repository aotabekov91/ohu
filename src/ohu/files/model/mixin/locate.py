from gizmo.vimo.model import mixin

class Locate(mixin.Locate):

    def getUniqLocator(self, data={}, kind=None):

        f=self.findLocator('getUniq', kind)
        if f: return f(data)
        data['hash']=self.id()
        data['kind']=self.kind
        return self.createLocator(data)
