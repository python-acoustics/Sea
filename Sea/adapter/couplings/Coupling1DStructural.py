import Sea
from Coupling import Coupling

class Coupling1DStructural(Coupling,Sea.model.couplings.Coupling1DStructural):
    """
    A coupling describing a structural connection of a single point.
    """
    name = 'Point'
    description = 'A coupling describing a connection of a single point.'
    
    
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
        return
    
        
#class CouplingArea(Coupling):
    #"""
    #A coupling describing a connection along a surface.
    #"""
    #name = 'Surface'
    #description = 'A coupling describing a connection along a surface.'
    
    #model = Sea.model.couplings.CouplingLine()

    #def __init__(self, obj, system, subsystem_from, subsystem_to, **properties):
        #Coupling.__init__(self, obj, system, subsystem_from, subsystem_to, **properties)
        
        
        
