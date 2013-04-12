
from ..base import ViewProviderBase

class ViewProviderConnection(ViewProviderBase):
    
    def claimChildren(self):
        return self.couplings()
        
    def couplings(self):
        """
        Return a list of couplings.
        
        :rtype: list
        """
        try:
            obj = self.obj.Object
        except AttributeError:
            return []
        print obj.couplings()    
        return obj.couplings()
    