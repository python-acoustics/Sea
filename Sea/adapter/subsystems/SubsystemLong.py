import abc

class SubsystemLong(object):
    """
    Adapter class for longitudinal wave subsystems.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj):
        obj.Component.Proxy.subsystem_long = obj.Proxy
    
    def onChanged(self, obj, prop):
        pass
    
    def execute(self, obj):
        pass