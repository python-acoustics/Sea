
from Subsystem import Subsystem
from SubsystemBend import SubsystemBend
from SubsystemStructural import SubsystemStructural

class SubsystemStructuralBend(Subsystem, SubsystemBend, SubsystemStructural):
    """Subsystem for bending waves in a structural component.
    """
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        SubsystemBend.__init__(self, obj)
        SubsystemStructural.__init__(self, obj)

    def onChanged(self, obj, prop):
        Subsystem.onChanged(self, obj, prop)
        SubsystemBend.onChanged(self, obj, prop)
        SubsystemStructural.onChanged(self, obj, prop)
    
    def execute(self, obj):
        Subsystem.execute(self, obj)
        SubsystemBend.execute(self, obj)
        SubsystemStructural.execute(self, obj)
