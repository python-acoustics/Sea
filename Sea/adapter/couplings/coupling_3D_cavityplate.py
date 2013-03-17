import Sea
from .. import baseclasses

class Coupling3DCavityPlate(baseclasses.Coupling):
    """
    A coupling describing the relation between a cavity and a plate.
    """
    name = "CavityToPlate"
    description = "A coupling describing the relation between a cavity and a plate."
    
    model = Sea.model.couplings.Coupling3DCavityPlate()
    
    def __init__(self, obj, system, connection, component_from, subsystem_from, component_to, subsystem_to):
        baseclasses.Coupling.__init__(self, obj, system, connection, component_from, subsystem_from, component_to, subsystem_to)
        
        
    def onChanged(self, obj, prop):
        baseclasses.Coupling.onChanged(self, obj, prop)
        
    def execute(self, obj):
        baseclasses.Coupling.execute(self, obj)
        
    