import Sea
from .. import baseclasses

class Coupling3DPlateCavity(baseclasses.Coupling):
    """
    A coupling describing the relation between a plate and a cavity.
    """
    name = "PlateToCavity"
    description = "A coupling describing the relation between a plate and a cavity."
    
    model = Sea.model.couplings.Coupling3DPlateCavity()
    
    def __init__(self, obj, system, connection, component_from, subsystem_from, component_to, subsystem_to):
        baseclasses.Coupling.__init__(self, obj, system, connection, component_from, subsystem_from, component_to, subsystem_to)
        
        
    def onChanged(self, obj, prop):
        baseclasses.Coupling.onChanged(self, obj, prop)
        
    def execute(self, obj):
        baseclasses.Coupling.execute(self, obj)
        
    