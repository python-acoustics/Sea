import abc

from Subsystem import Subsystem


class SubsystemLong(Subsystem):
    """
    Adapter class for longitudinal wave subsystems.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        component.Proxy.subsystem_long = obj.Proxy
        