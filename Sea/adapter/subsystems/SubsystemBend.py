import abc

class SubsystemBend(object):
    """
    Adapter class for bending wave subsystems.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj):
        obj.Component.Proxy.subsystem_bend = obj.Proxy

    def onChanged(self, obj, prop):
        pass
    
    def execute(self, obj):
        pass