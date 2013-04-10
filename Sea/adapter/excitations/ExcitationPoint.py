import Sea
from Excitation import Excitation

class ExcitationPoint(Excitation, Sea.model.excitations.ExcitationPoint):
    """
    Rain on the roof excitation
    """

    name = 'Point'
    description = 'An excitation of a single point.'
    
    def __init__(self, obj, system, subsystem):
        Excitation.__init__(self, obj, system, subsystem)
        
        
