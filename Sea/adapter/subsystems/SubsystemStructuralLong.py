

from Subsystem import Subsystem
from SubsystemLong import SubsystemLong
from SubsystemStructural import SubsystemStructural

class SubsystemStructuralLong(Subsystem, SubsystemLong, SubsystemStructural):
    """Subsystem for longitudinal waves in a structural component.
    """
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        SubsystemLong.__init__(self, obj)
        SubsystemStructural.__init__(self, obj)

    def onChanged(self, obj, prop):
        Subsystem.onChanged(self, obj, prop)
        SubsystemLong.onChanged(self, obj, prop)
        SubsystemStructural.onChanged(self, obj, prop)
    
    def execute(self, obj):
        Subsystem.execute(self, obj)
        SubsystemLong.execute(self, obj)
        SubsystemStructural.execute(self, obj)
