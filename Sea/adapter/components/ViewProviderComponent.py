

from ..base import ViewProviderBase

class ViewProviderComponent(ViewProviderBase):
    
    def claimChildren(self):
        sub = self.subsystems()
        print sub
        return sub
        
    def subsystems(self):
        """
        Return a list of subsystems.
        
        :rtype: list
        """
        try:
            obj = self.obj.Object
        except AttributeError:
            return []
            
        viewproviders = obj.subsystems()
        print viewproviders
        
        return viewprovider