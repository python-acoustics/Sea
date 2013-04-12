
from ..base import ViewProviderBase

class ViewProviderSystem(ViewProviderBase):
    
    def claimChildren(self):
        try:
            return self.obj.Object.InList + [self.obj.Object.Frequency]
        except AttributeError:
            return []
        