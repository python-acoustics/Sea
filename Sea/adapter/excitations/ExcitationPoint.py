import Sea
from .. import baseclasses

class ExcitationPoint(baseclasses.Excitation):
    """
    Rain on the roof excitation
    """

    name = 'Point'
    description = 'An excitation of a single point.'
    
    model = Sea.model.excitations.ExcitationPoint
    
    def __init__(self, obj, system, subsystem):
        baseclasses.Excitation.__init__(self, obj, system, subsystem)
        
        
