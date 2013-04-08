import abc

from Subsystem import Subsystem


class SubsystemShear(Subsystem):
    """
    Adapter class for shear wave subsystems.
    """
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        component.Proxy.subsystem_shear = obj.Proxy
        
                   