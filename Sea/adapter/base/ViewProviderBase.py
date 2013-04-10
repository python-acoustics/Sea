import abc

class ViewProviderBase(object):
    """
    Abstract base class for ViewProviders
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj):
        """Constructor
        
        :param obj: Object
        :type obj: :class:`FreeCAD.ViewObject` 
        """
        obj.Proxy = self
        self.obj = obj

    def claimChildren(self):
        """
        Return tree children.
        
        :rtype: list
        """
        return []
        
    def attach(self, obj):
        pass
      
    def onChanged(self, obj, prop):
        pass
