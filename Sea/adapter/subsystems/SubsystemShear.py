import abc

class SubsystemShear(object):
    """
    Adapter class for shear wave subsystems.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj):
        obj.Component.Proxy.subsystem_shear = obj.Proxy
        
        
    def onChanged(self, obj, prop):
        pass
    
    def execute(self, obj):
        pass
        
                   