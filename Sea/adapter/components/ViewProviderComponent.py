
from ..base import ViewProviderBase

class ViewProviderComponent(ViewProviderBase):
    
    def claimChildren(self):
        return self.subsystems()
        
    def subsystems(self):
        """
        Return a list of subsystems.
        
        :rtype: list
        """
        try:
            obj = self.obj.Object
        except AttributeError:
            return []
            
        return obj.subsystems()
        