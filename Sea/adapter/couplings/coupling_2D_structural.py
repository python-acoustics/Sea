import Sea
from .. import baseclasses

class Coupling2DStructural(baseclasses.Coupling):
    """
    A coupling describing a connection along a line.
    """
    name = 'Line'
    description = 'A coupling describing a connection along a line.'

    model = Sea.model.couplings.Coupling2DStructural()

    def __init__(self, obj, connection, component_from, component_to, subsystem_from, subsystem_to):
        baseclasses.Coupling.__init__(self, obj, connection, component_from, component_to, subsystem_from, subsystem_to)

    
    def onChanged(self, obj, prop):
        baseclasses.Coupling.onChanged(self, obj, prop)
        
    
    def execute(self, obj):
        baseclasses.Coupling.execute(self, obj)
    
    
    @staticmethod
    def size(obj):
        """
        Return the size of the coupling.
        
        :param obj: an instance of :class:`Sea.adapter.couplings.CouplingPoint`
        
        """
        return 0.0