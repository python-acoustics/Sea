import Sea
from .. import baseclasses

class Coupling2DStructural(baseclasses.Coupling):
    """
    A coupling describing a connection along a line.
    """
    name = 'Line'
    description = 'A coupling describing a connection along a line.'

    model = Sea.model.couplings.Coupling2DStructural()

    def __init__(self, obj, system, connection, component_from, component_to, subsystem_from, subsystem_to):
        baseclasses.Coupling.__init__(self, obj, system, connection, component_from, component_to, subsystem_from, subsystem_to)

    @staticmethod
    def size(obj):
        """
        Return the size of the coupling.
        
        :param obj: an instance of :class:`Sea.adapter.couplings.CouplingPoint`
        
        """
        return