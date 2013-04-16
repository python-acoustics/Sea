
from ..base import ViewProviderBase

class ViewProviderConnection(ViewProviderBase):
    
    def claimChildren(self):
        obj = self.obj.Object
        
        children = list()
        try:
            for item in obj.InList:
                if Sea.adapter.document._isObject(self.sort):
                    children.append(item)
        
        except AttributeError:
            pass
        return children
        
    