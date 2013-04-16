
from Subsystem import Subsystem
from SubsystemLong import SubsystemLong
from SubsystemCavity import SubsystemCavity


class SubsystemCavityLong(Subsystem, SubsystemLong, SubsystemCavity):
    """Subsystem for longitudinal waves in a cavity.
    """
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        SubsystemLong.__init__(self, obj)
        SubsystemCavity.__init__(self, obj)

    def onChanged(self, obj, prop):
        Subsystem.onChanged(self, obj, prop)
        SubsystemLong.onChanged(self, obj, prop)
        SubsystemCavity.onChanged(self, obj, prop)
    
    def execute(self, obj):
        Subsystem.execute(self, obj)
        SubsystemLong.execute(self, obj)
        SubsystemCavity.execute(self, obj)
        