import abc

from Subsystem import Subsystem


class SubsystemBend(Subsystem):
    """
    Adapter class for bending wave subsystems.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        component.Proxy.subsystem_bend = obj.Proxy
