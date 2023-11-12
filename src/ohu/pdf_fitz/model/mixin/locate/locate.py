from gizmo.vimo.model import mixin

class Locate(mixin.Locate):

    def getUniqLocator(self, data=None, kind=None):

        f=self.findLocator('getUniq', kind)
        if f: return f(data)
        return {'hash': self.id(), 'kind': self.kind}
