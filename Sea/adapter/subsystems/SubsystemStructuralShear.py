
from Subsystem import Subsystem
from SubsystemShear import SubsystemShear
from SubsystemStructural import SubsystemStructural

class SubsystemStructuralShear(Subsystem, SubsystemShear, SubsystemStructural):
    """Subsystem for shear waves in a structural component.
    """
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        SubsystemShear.__init__(self, obj)
        SubsystemStructural.__init__(self, obj)

    def onChanged(self, obj, prop):
        Subsystem.onChanged(self, obj, prop)
        SubsystemShear.onChanged(self, obj, prop)
        SubsystemStructural.onChanged(self, obj, prop)
    
    def execute(self, obj):
        Subsystem.execute(self, obj)
        SubsystemShear.execute(self, obj)
        SubsystemStructural.execute(self, obj)
