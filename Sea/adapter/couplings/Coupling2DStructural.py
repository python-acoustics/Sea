import Sea
from Coupling import Coupling

class Coupling2DStructural(Coupling, Sea.model.couplings.Coupling2DStructural):
    """
    A coupling describing a structural connection along a line.
    """
    name = 'Line'
    description = 'A coupling describing a connection along a line.'

    def __init__(self, obj, connection, subsystem_from, subsystem_to):
        Coupling.__init__(self, obj, connection, subsystem_from, subsystem_to)

    
    def onChanged(self, obj, prop):
        Coupling.onChanged(self, obj, prop)
        
    
    def execute(self, obj):
        Coupling.execute(self, obj)
    
    
    @staticmethod
    def size(obj):
        """
        Return the size of the coupling.
        
        :param obj: an instance of :class:`Sea.adapter.couplings.CouplingPoint`
        
        """
        return 0.0